using CALiPPSO
using HiGHS

const tol_optimality = CALiPPSO.default_tol_optimality
const max_threads = CALiPPSO.max_threads
const highs_opt = HiGHS.Optimizer()
const highs_attributes = Dict(
    "small_matrix_value" => 0.1 * tol_optimality,
    "primal_feasibility_tolerance" => tol_optimality,
    "dual_feasibility_tolerance" => tol_optimality,
    "solver" => "ipm",
    "ipm_optimality_tolerance" => tol_optimality,
    "threads" => max_threads,
    "parallel" => "on",
    "output_flag" => false,
)

precompile_main_function(highs_opt, highs_attributes)

using Random
Random.seed!(123) # same seed as run_mwe.jl -> identical packing

const d, N, φ0, L = 3, 512, 0.3, 1.0
r0, Xs0 = generate_random_configuration(d, N, φ0, L)

packing, info, Γ_vs_t, Smax_vs_t, isostatic_vs_t = produce_jammed_configuration!(Xs0, r0;
            ℓ0=0.2*L, max_iters=500, tol_Γ_convergence=1e-12,
            optimizer=highs_opt, solver_attributes=highs_attributes)

# ---- Export final configuration ----
positions = CALiPPSO.get_positions(packing)      # Vector{SVector{d,PeriodicNumber}}
R = packing.R
Lbox = positions[1][1].L

# Coordination number per particle (0 for rattlers)
zs = CALiPPSO.get_coordination_number.(packing.Particles)

open("packing_d3_N512.csv", "w") do io
    println(io, "# d=$d N=$N L=$Lbox R=$R phi=$(packing_fraction(packing))")
    println(io, "x,y,z,coordination")
    for (p, z) in zip(positions, zs)
        x, y, zc = p[1].value, p[2].value, p[3].value
        println(io, "$x,$y,$zc,$z")
    end
end

println("EXPORTED $(length(positions)) particles to packing_d3_N512.csv")
println("R = $R,  L = $Lbox,  phi = $(packing_fraction(packing))")

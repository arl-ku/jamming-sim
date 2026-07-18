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
Random.seed!(123) # same seed as run_mwe.jl / export_packing.jl

const d, N, φ0, L = 3, 512, 0.3, 1.0
r0, Xs0 = generate_random_configuration(d, N, φ0, L)

# trajectory sink: each frame is (R, d×N matrix of raw coordinates)
traj = Vector{Tuple{Float64,Matrix{Float64}}}()

packing, info, Γ_vs_t, Smax_vs_t, isostatic_vs_t = produce_jammed_configuration!(Xs0, r0;
            ℓ0=0.2*L, max_iters=500, tol_Γ_convergence=1e-12,
            optimizer=highs_opt, solver_attributes=highs_attributes,
            traj_sink=traj)

println("\nCaptured $(length(traj)) frames")

# ---- Write compact JSON: metadata + frames ----
# To keep the file small we subsample frames adaptively (dense early where motion is large).
nf = length(traj)
# keep every frame up to 40, then every 3rd, always include the last
keep = Int[]
for k in 1:nf
    if k <= 40 || k % 3 == 0 || k == nf
        push!(keep, k)
    end
end
unique!(keep)

open("packing_trajectory.json", "w") do io
    Rfinal = packing.R
    write(io, "{\n")
    write(io, "\"d\":$d,\"N\":$N,\"L\":$L,\"phi0\":$φ0,")
    write(io, "\"phiFinal\":$(packing_fraction(packing)),")
    write(io, "\"Rfinal\":$Rfinal,\"nframesTotal\":$nf,")
    # coordination number only meaningful at the end; export it for final-frame coloring
    zs = CALiPPSO.get_coordination_number.(packing.Particles)
    write(io, "\"coord\":[" * join(zs, ",") * "],")
    write(io, "\"frames\":[\n")
    for (fi, k) in enumerate(keep)
        R, pos = traj[k]
        # flatten column-major particle by particle: x1,y1,z1, x2,y2,z2 ...
        vals = Vector{String}(undef, N*d)
        idx = 1
        for i in 1:N, c in 1:d
            vals[idx] = string(round(pos[c, i], digits=4)); idx += 1
        end
        write(io, "{\"i\":$(k-1),\"R\":$(round(R, digits=6)),\"p\":[" * join(vals, ",") * "]}")
        write(io, fi == length(keep) ? "\n" : ",\n")
    end
    write(io, "]\n}\n")
end

println("EXPORTED trajectory ($(length(keep)) kept frames) to packing_trajectory.json")
println("R: $(traj[1][1])  ->  $(packing.R)")
println("phi: $φ0  ->  $(packing_fraction(packing))")

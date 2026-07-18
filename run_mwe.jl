using CALiPPSO
using HiGHS

# HiGHS is a robust open-source LP solver supported by CALiPPSO.
# (The default GLPK solver segfaults on this platform for larger systems.)
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

precompile_main_function(highs_opt, highs_attributes) # optional; colorful output can be ignored

using Random
Random.seed!(123) # reproducibility

const d, N, φ0, L = 3, 512, 0.3, 1.0
r0, Xs0 = generate_random_configuration(d, N, φ0, L)

println("\n\n========== RUNNING CALiPPSO (HiGHS solver) ==========\n")
packing, info, Γ_vs_t, Smax_vs_t, isostatic_vs_t = produce_jammed_configuration!(Xs0, r0;
            ℓ0=0.2*L, max_iters=500, tol_Γ_convergence=1e-12,
            optimizer=highs_opt, solver_attributes=highs_attributes)

isostatic, Nc, Nnr = is_isostatic(packing)
println("\n\n========== RESULTS ==========")
println("Converged?               : ", info.converged)
println("Iterations               : ", info.iterations)
println("Total time (s)           : ", round(info.time, digits=3))
println("Initial packing fraction : ", φ0)
println("Final packing fraction φ : ", round(packing_fraction(packing), digits=5))
println("Isostatic packing?       : ", isostatic)
println("Contacts / non-rattlers  : ", Nc, " / ", Nnr)
println("Final sqrt(Γ*)           : ", Γ_vs_t[end])
println("Final max gap s*         : ", Smax_vs_t[end])
println("\nDONE")

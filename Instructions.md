1. Replace synthetic data with public benchmarks: Download ISCX VPN/non-VPN (2016) and USTC-TFC (2016). Preprocess PCAPs to extract the exact 8 features used in the paper (inter-arrival time, packet size, protocol, flow duration, total bytes, packet count, dst port, TTL). Provide dataset statistics (samples per class, flow durations).  
   Deliverable: New "Dataset" subsection with table of real dataset stats.

2. Add deep learning baselines: Implement and run CNN (1D), LSTM, and ET-BERT (or a simpler Transformer) on the same datasets. Report their accuracy AND estimate their composite overhead *F* (using the paper's formulas for weight density, etc.). Show that MOPSO-FFNN-AD matches/exceeds them while offering lower overhead.  
   Deliverable: New rows in Table 6 (SOTA comparison) with deep learning methods.

3. Implement k-fold Cross-Validation: The current paper uses a fixed train/val/test split. Run 10-fold stratified cross-validation on the real datasets. Report the mean and standard deviation of Accuracy and *F* across all folds. Perform paired t-tests against PSO-FFNN to prove significance (p \< 0.05).  
   Deliverable: Updated Table 2 with mean ± std metrics and p-values.

4. Ablation study on fitness weights: The paper uses fixed weights (α=0.45, β=0.20, ...). Vary these weights to simulate 3 deployment scenarios: (1) Accuracy-critical (α=0.8), (2) Bandwidth-constrained (ε=0.5), (3) Latency-sensitive (δ=0.5). Show how the Pareto front shifts for each scenario.  
   Deliverables: A new figure (Pareto fronts for 3 deployment policies).

5. Feature importance analysis: Use the trained FFNN weights to compute feature importance (e.g., using Garson's algorithm or permutation importance). Identify which of the 8 features are most responsible for accuracy vs. overhead.  
   Deliverables: A bar chart in the results section showing feature contribution.

6. Ensure lemmas (1 & 2\) are correctly typeset and explain why stability matters for SDWN controllers.

7. Discuss: (i) dependency on feature engineering (vs. raw bytes), (ii) training time of MOPSO vs. simple SGD, (iii) generalization to QUIC/TLS 1.3 traffic.

8. Package all code (data preprocessing, Mininet scripts, MOPSO optimizer) into a GitHub repository with a README. Prepare an Appendix with all hyperparameter grids and full confusion matrices.
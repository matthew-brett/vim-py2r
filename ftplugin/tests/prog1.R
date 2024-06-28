density <- c(.02, .026, .023, .017, .022, .019, .018, .018, .017, .022)

n_density <- length(density)

n_trials <- 10000
results <- numeric(n_trials)

for (i in 1:n_trials) {
    fake_density <- sample(density, size=n_density, replace=TRUE)
    results[i] <- mean(fake_density)
}

hist(results, breaks=25,
    main='Bootstrap distribution of density means',
    xlab='Bootstrap density means')

mean_limits <- quantile(results, c(0.025, 0.975))

message('95% percent limits for mean: ', mean_limits)

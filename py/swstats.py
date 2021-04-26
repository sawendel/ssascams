# From http://ethen8181.github.io/machine-learning/ab_tests/frequentist_ab_test.html#Comparing-Two-Proportions

# See https://towardsdatascience.com/python-code-from-hypothesis-test-to-online-experiments-with-buiness-cases-e0597c6d1ec

import statsmodels.stats.api as sms


def two_proprotions_test(success_a, size_a, success_b, size_b):
    """
    A/B test for two proportions;
    given a success a trial size of group A and B compute
    its zscore and pvalue

    Parameters
    ----------
    success_a, success_b : int
        Number of successes in each group

    size_a, size_b : int
        Size, or number of observations in each group

    Returns
    -------
    zscore : float
        test statistic for the two proportion z-test

    pvalue : float
        p-value for the two proportion z-test
    """
    prop_a = success_a / size_a
    prop_b = success_b / size_b
    prop_pooled = (success_a + success_b) / (size_a + size_b)
    var = prop_pooled * (1 - prop_pooled) * (1 / size_a + 1 / size_b)
    zscore = np.abs(prop_b - prop_a) / np.sqrt(var)
    one_side = 1 - stats.norm(loc = 0, scale = 1).cdf(zscore)
    pvalue = one_side * 2
    return zscore, pvalue


def demo_two_proprotions_test():
    success_a = 486
    size_a = 5000
    success_b = 527
    size_b = 5000

    zscore, pvalue = two_proprotions_test(success_a, size_a, success_b, size_b)
    print('zscore = {:.3f}, pvalue = {:.3f}'.format(zscore, pvalue))



def compute_sample_size(prop1, min_diff, significance=0.05, power=0.8):
    """
    Computes the sample sized required for a two-proportion A/B test;
    result matches R's pwr.2p.test from the pwr package

    Parameters
    ----------
    prop1 : float
        The baseline proportion, e.g. conversion rate

    min_diff : float
        Minimum detectable difference

    significance : float, default 0.05
        Often denoted as alpha. Governs the chance of a false positive.
        A significance level of 0.05 means that there is a 5% chance of
        a false positive. In other words, our confidence level is
        1 - 0.05 = 0.95

    power : float, default 0.8
        Often denoted as beta. Power of 0.80 means that there is an 80%
        chance that if there was an effect, we would detect it
        (or a 20% chance that we'd miss the effect)

    Returns
    -------
    sample_size : int
        Required sample size for each group of the experiment

    References
    ----------
    R pwr package's vignette
    - https://cran.r-project.org/web/packages/pwr/vignettes/pwr-vignette.html

    Stackoverflow: Is there a python (scipy) function to determine parameters
    needed to obtain a target power?
    - https://stackoverflow.com/questions/15204070/is-there-a-python-scipy-function-to-determine-parameters-needed-to-obtain-a-ta
    """
    prop2 = prop1 + min_diff
    effect_size = sms.proportion_effectsize(prop1, prop2)
    sample_size = sms.NormalIndPower().solve_power(
        effect_size, power=power, alpha=significance, ratio=1)

    return sample_size

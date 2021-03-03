"""
Tests for the partner selection approaches from the Copula module.
"""
import os
import unittest
import pandas as pd

from statsmodels.distributions.empirical_distribution import ECDF
from arbitragelab.copula_approach.vine_copula_partner_selection import PartnerSelection
from arbitragelab.copula_approach.vine_copula_partner_selection_utils import get_sum_correlations, multivariate_rho, \
    diagonal_measure, extremal_measure, get_co_variance_matrix


class PartnerSelectionTests(unittest.TestCase):
    """
    Tests Partner Selection Approaches.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Creates dataframes with returns and quantile data to work with corresponding test cases.
        """

        project_path = os.path.dirname(__file__)
        data_path = project_path + '/test_data/sp500_2016_test.csv'
        cls.quadruple = ['A', 'AAL', 'AAP', 'AAPL']
        prices = pd.read_csv(data_path, parse_dates=True, index_col='Date').dropna()
        cls.ps = PartnerSelection(prices)

        cls.u = cls.ps.returns.copy()
        for column in cls.ps.returns.columns:
            ecdf = ECDF(cls.ps.returns.loc[:, column])
            cls.u[column] = ecdf(cls.ps.returns.loc[:, column])

        cls.co_variance_matrix = get_co_variance_matrix()

    def test_sum_correlations(self):
        """
        Tests Traditional Approach.
        """
        self.assertEqual(round(get_sum_correlations(self.ps.correlation_matrix, self.quadruple), 4), 1.9678)

    def test_multivariate_rho(self):
        """
        Tests Extended Approach.
        """
        self.assertEqual(round(multivariate_rho(self.u[self.quadruple]), 4), 0.3114)

    def test_diagonal_measure(self):
        """
        Tests Geometric Approach.
        """
        self.assertEqual(round(diagonal_measure(self.ps.ranked_returns[self.quadruple]), 4), 91.9374)

    def test_extremal_measure(self):
        """
        Tests Extremal Approach.
        """
        self.assertEqual(round(extremal_measure(self.ps.ranked_returns[self.quadruple], self.co_variance_matrix), 4), 108.5128)

if __name__ == '__main__':
    unittest.main()

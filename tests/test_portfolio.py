from src.portfolio.portfolio import Security, Portfolio


class TestPortfolio:
    def test_portfolio(self):
        subject = Portfolio(portfolio_source='TEST')
        assert subject.holdings == {}


class TestSecurity:
    def test_security(self):
        subject = Security.build('AAPL', 'Apple', 10, 100, 50, 1000)
        assert subject.symbol == 'AAPL'
        assert subject.name == 'Apple'
        assert subject.quantity == 10
        assert subject.last_price == 100
        assert subject.avg_price_paid == 50
        assert subject.total_value == 1000
        assert subject.total_return() == 500
        assert subject.to_dict() == {
            'symbol': 'AAPL',
            'name': 'Apple',
            'quantity': 10,
            'last_price': 100,
            'avg_price_paid': 50,
            'total_value': 1000,
            'total_return': 500,
        }

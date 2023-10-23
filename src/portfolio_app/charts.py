
from altair import Chart as AltairChart
import altair as alt
from pandas import DataFrame


class ChartManager:

    @staticmethod
    def get_pie_chart(df: DataFrame, value_col='Percentage') -> AltairChart:
        df = df.reset_index()
        chart = alt.Chart(df).mark_arc(innerRadius=50).encode(
            theta=value_col,
            color=alt.Color('index:N', legend=alt.Legend(title="Index")),
            tooltip=['index', value_col]
        ).properties(
            width=400,
            height=400
        )
        return chart
    

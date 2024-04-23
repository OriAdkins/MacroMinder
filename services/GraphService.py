import plotly.graph_objects as go
from services.HabitService import HabitService
from services.CompletionLogService import CompletionLogService

class GraphService:

    def generate_habit_progress_graph(current_date, user_id):
        total_habits = HabitService.count_total_habits_for_user(current_date, user_id)
        completed_habits = HabitService.count_completed_habits_for_user(current_date, user_id)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Completed Habits'],
            y=[completed_habits],
            name='Completed',
            marker_color='rgb(55, 83, 109)'
        ))

        fig.update_layout(
            title='Habit Progress',
            xaxis=dict(title=''),
            yaxis=dict(title='Total Habits for Today', range=[0, total_habits])
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html

    def generate_weight_over_time_graph(user_id):
        dates, weights = CompletionLogService.fetch_weight_data(user_id)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=weights, mode='lines', name='Weight'))

        fig.update_layout(
            title='Weight Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Weight (lbs)', range=[0, 300]),
            height=300,
            width=350,
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html
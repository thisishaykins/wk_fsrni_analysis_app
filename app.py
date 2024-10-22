import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Path to your JSON file
# file_path = 'data/FlightNoItinenaryFoond.json'
file_path = 'data/FlightSearchRequestNoItinerary.json'

# Try to load the JSON file while ignoring errors
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            json_data = json.load(file)  # Load JSON data
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            json_data = []
except FileNotFoundError:
    print(f"File not found: {file_path}")
    json_data = []

# If the JSON loaded successfully, proceed with normalization
if json_data:
    try:
        # Normalize the JSON data into a DataFrame
        df = pd.json_normalize(json_data, sep='_')

        # Extract relevant fields for the report
        df['Timestamp'] = pd.to_datetime(df['Timestamp_$date'])
        df['Departure'] = df['SearchPayload_Itineraries'].apply(lambda x: x[0]['Departure'])
        df['Destination'] = df['SearchPayload_Itineraries'].apply(lambda x: x[0]['Destination'])
        df['DepartureDate'] = pd.to_datetime(df['SearchPayload_Itineraries'].apply(lambda x: x[0]['DepartureDate']['$date']))
        df['Adults'] = df['SearchPayload_Adults']
        df['Children'] = df['SearchPayload_Children']
        df['Infants'] = df['SearchPayload_Infants']
        df['TicketClass'] = df['SearchPayload_Itineraries'].apply(lambda x: x[0]['Ticketclass'])
        df['Source'] = df['Source']

        # Summarize total searches with no results
        total_no_results = df.shape[0]

        # Group by departure and destination airports
        airport_breakdown = df.groupby(['Departure', 'Destination']).size().reset_index(name='no_results_count')

        # Group by date of departure
        date_breakdown = df.groupby('DepartureDate').size().reset_index(name='no_results_count')

        # Group by passenger count
        passenger_breakdown = df.groupby(['Adults', 'Children', 'Infants']).size().reset_index(name='no_results_count')

        # Group by ticket class
        ticket_class_breakdown = df.groupby('TicketClass').size().reset_index(name='no_results_count')

        # Display summary
        print(f"Total number of searches with no results: {total_no_results}")
        print("\nBreakdown by Airports:\n", airport_breakdown)
        print("\nBreakdown by Departure Date:\n", date_breakdown)
        print("\nBreakdown by Passenger Count:\n", passenger_breakdown)
        print("\nBreakdown by Ticket Class:\n", ticket_class_breakdown)

        # Export summaries to CSV files

        # Export airport breakdown
        airport_breakdown.to_csv('exports/airport_breakdown_report.csv', index=False)

        # Export date breakdown
        date_breakdown.to_csv('exports/date_breakdown_report.csv', index=False)

        # Export passenger breakdown
        passenger_breakdown.to_csv('exports/passenger_breakdown_report.csv', index=False)

        # Export ticket class breakdown
        ticket_class_breakdown.to_csv('exports/ticket_class_breakdown_report.csv', index=False)

        print("Summaries exported to CSV files.")


        """
        Seaborn graphs and charts
        """
        # Bar chart for airport breakdown
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Departure', y='no_results_count', hue='Destination', data=airport_breakdown)
        plt.title('No Results Count by Departure and Destination Airports')
        plt.xlabel('Departure Airport')
        plt.ylabel('No Results Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('exports/seaborn-charts/airport_breakdown_chart.png')
        plt.show()

        # Line chart for breakdown by departure date
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='DepartureDate', y='no_results_count', data=date_breakdown, marker='o')
        plt.title('No Results Count by Departure Date')
        plt.xlabel('Departure Date')
        plt.ylabel('No Results Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('exports/seaborn-charts/date_breakdown_chart.png')
        plt.show()

        # Bar chart for passenger breakdown (adults, children, infants)
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Adults', y='no_results_count', hue='Children', data=passenger_breakdown)
        plt.title('No Results Count by Passenger Count (Adults/Children)')
        plt.xlabel('Number of Adults')
        plt.ylabel('No Results Count')
        plt.tight_layout()
        plt.savefig('exports/seaborn-charts/passenger_breakdown_chart.png')
        plt.show()

        # Bar chart for passenger breakdown (adults, children, infants)
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Adults', y='no_results_count', hue='Children', data=passenger_breakdown)
        plt.title('No Results Count by Passenger Count (Adults/Children)')
        plt.xlabel('Number of Adults')
        plt.ylabel('No Results Count')
        plt.tight_layout()
        plt.savefig('exports/seaborn-charts/passenger_breakdown_chart.png')
        plt.show()

        # Pie chart for ticket class breakdown
        plt.figure(figsize=(7, 7))
        plt.pie(ticket_class_breakdown['no_results_count'], labels=ticket_class_breakdown['TicketClass'],
                autopct='%1.1f%%')
        plt.title('No Results Count by Ticket Class')
        plt.tight_layout()
        plt.savefig('exports/seaborn-charts/ticket_class_breakdown_chart.png')
        plt.show()


    except ValueError as e:
        print(f"Error processing data: {e}")
else:
    print("No valid data to process.")
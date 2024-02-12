import pandas as pd
import matplotlib.pyplot as plt

# Načtení dat z Excel souboru
data_path = 'data/klementinum.xlsx'
data_sheet_name = 'data'
temperature_data = pd.read_excel(data_path, sheet_name=data_sheet_name)


class TemperatureAnalytics:
    def __init__(self, data):
        self.data = data

    def get_average_temperature(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            print("Zadán nesprávný rok")
            return None
        return round(yearly_data['T-AVG'].mean(), 2)

    def get_min_max_temperature(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            return None, None, None
        max_temp = yearly_data['TMA'].max()
        min_temp = yearly_data['TMI'].min()
        return min_temp, max_temp

    def get_monthly_averages(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            print("Zadán nesprávný rok")
            return None
        return yearly_data.groupby('měsíc')['T-AVG'].mean()

    def analyze_temperature_trends(self, start_year, end_year):
        trend_data = self.data[(self.data['rok'] >= start_year) & (self.data['rok'] <= end_year)]
        return trend_data.groupby('rok')['T-AVG'].mean()

    def detect_temperature_anomalies(self):
        max_month_temps = self.data.groupby('měsíc')['TMA'].mean()
        return self.data[self.data['TMA'] > max_month_temps[self.data['měsíc']].values]

    def plot_annual_temperature_averages(self, start_year, end_year):
        filtered_data = self.data[(self.data['rok'] >= start_year) & (self.data['rok'] <= end_year)]
        annual_avg_temps = filtered_data.groupby('rok')['T-AVG'].mean()
        plt.figure(figsize=(10, 6))
        plt.plot(annual_avg_temps.index, annual_avg_temps.values, marker='o', linestyle='-', color='b')
        plt.title(f'Průměrné roční teploty mezi lety {start_year} a {end_year}')
        plt.xlabel('Rok')
        plt.ylabel('Průměrná teplota (°C)')
        plt.grid(True)
        plt.show()


def main():
    temperature_analytics = TemperatureAnalytics(temperature_data)

    while True:
        print("Interaktivní menu pro analýzu teplot")
        print("1 - Zobrazit průměrnou teplotu pro zadaný rok")
        print("2 - Zobrazit minimální a maximální teplotu pro zadaný rok")
        print("3 - Zobrazit měsíční průměry pro zadaný rok")
        print("4 - Analyzovat teplotní trendy")
        print("5 - Analyzovat sezónní změny")
        print("6 - Detekovat teplotní anomálie")
        print("7 - Vykreslit průměrné roční teploty")
        print("0 - Konec")

        user_input = input("Zadejte vaši volbu: ")

        if user_input == "1":
            year_input = int(input("Zadejte rok (mezi 1775 a 2022): "))
            average_temp = temperature_analytics.get_average_temperature(year_input)
            if average_temp is not None:
                print(f"Průměrná teplota v roce {year_input}: {average_temp}°C")

        elif user_input == "2":
            year_input = int(input("Zadejte rok (mezi 1775 a 2022): "))
            min_temp, max_temp = temperature_analytics.get_min_max_temperature(year_input)
            if min_temp is not None:
                print(f"Minimální teplota v roce {year_input}: {min_temp}°C")
                print(f"Maximální teplota v roce {year_input}: {max_temp}°C")

        elif user_input == "3":
            year_input = int(input("Zadejte rok (mezi 1775 a 2022): "))
            monthly_averages = temperature_analytics.get_monthly_averages(year_input)
            if monthly_averages is not None:
                print(f"Měsíční průměry pro rok {year_input}:")
                print(monthly_averages)

        elif user_input == "4":
            start_year = int(input("Zadejte začáteční rok (mezi 1775 a 2022): "))
            end_year = int(input("Zadejte konečný rok (mezi 1775 a 2022): "))
            trends = temperature_analytics.analyze_temperature_trends(start_year, end_year)
            print("Teplotní trendy:")
            print(trends)

        elif user_input == "5":
            print("Funkcionalita pro analýzu sezónních změn zatím není implementována.")

        elif user_input == "6":
            anomalies = temperature_analytics.detect_temperature_anomalies()
            print("Detekovány teplotní anomálie:")
            print(anomalies)

        elif user_input == "7":
            start_year = int(input("Zadejte začáteční rok (mezi 1775 a 2022): "))
            end_year = int(input("Zadejte konečný rok (mezi 1775 a 2022): "))
            temperature_analytics.plot_annual_temperature_averages(start_year, end_year)

        elif user_input == "0":
            print("Program bude ukončen.")
            break

        else:
            print("Nesprávný vstup")


if __name__ == '__main__':
    main()
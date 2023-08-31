import numpy as np
import pandas as pd
import warnings
import streamlit as st
from PIL import Image
warnings.simplefilter(action='ignore', category=FutureWarning)

def round_price_step(x):
    if x < 20:
        return np.floor(x * 100) / 100
    elif x < 50:
        return np.floor(x * 50) / 50
    elif x < 100:
        return np.floor(x * 20) / 20
    else:
        return np.floor(x * 10) / 10

def round_price_step_update(x):
    if x < 20:
        return np.floor(x * 100) / 100
    elif x < 50:
        return np.floor(x * 50) / 50
    elif x < 100:
        return np.floor(x * 20) / 20
    elif x < 250:
        return np.floor(x * 10) / 10
    elif x < 500:
        return np.floor(x * 4) / 4
    elif x < 1000:
        return np.floor(x * 2) / 2
    elif x < 2500:
        return int(x)
    else:
        return x - (x % 2.5)
    
def add_ceiling(x):
    return x * 1.1

def daily_profit(current_price, previous_price, lot_count):
    return (current_price - previous_price) * lot_count

def total_profit(current_price, initial_price, lot_count):
    return (current_price - initial_price) * lot_count

def simulate_trades(days, initial_price, lot_count):
    df = pd.DataFrame(columns=['tavan_sayisi', 'tavan_fiyati', 'gunluk_kar', 'toplam_kar', 'toplam_kar_yuzdesi'])
    previous_price = 0
    current_price = 0

    for i in range(days):
        if current_price == 0:
            current_price = round_price_step(add_ceiling(initial_price))
            previous_price = initial_price
        else:
            previous_price = current_price
            current_price = round_price_step(add_ceiling(current_price))

        daily_profit_value = daily_profit(current_price, previous_price, lot_count)
        total_profit_value = total_profit(current_price, initial_price, lot_count)
        total_profit_percentage = total_profit_value / (initial_price * lot_count) * 100

        df.loc[len(df.index)] = [i+1, current_price, daily_profit_value, total_profit_value, total_profit_percentage]

    return df

def calculate_lot_count_and_budget(initial_price, number_of_lots):
    number_of_participants = [1000000, 1200000, 1500000, 1700000, 
                              2000000, 2100000, 2200000, 2400000, 2500000]
    number_of_parts = ['1 milyon', '1.2 milyon', '1.5 milyon', '1.7 milyon',
                       '2 milyon', '2.1 milyon', '2.2 milyon', '2.4 milyon', '2.5 milyon']
    df = pd.DataFrame(columns=['number_of_participants', 'lot_count', 'budget'])

    for idx, num in enumerate(number_of_participants):
        lot_for_each_participant = number_of_lots / num
        if lot_for_each_participant % 1 != 0:
            upper_lot_count = np.ceil(lot_for_each_participant)
            lower_lot_count = np.floor(lot_for_each_participant)
            upper_lot_budget = upper_lot_count * initial_price
            lower_lot_budget = lower_lot_count * initial_price
            lot_count = f'{int(lower_lot_count)} lot - {int(upper_lot_count)} lot arası'
            budget = f'{int(lower_lot_budget)} ₺ - {int(upper_lot_budget)} ₺ arası'
        else:
            lot_count = f'{lot_for_each_participant} lot'
            budget = f'{lot_for_each_participant * initial_price} ₺'
   
        df.loc[len(df.index)] = [f'{number_of_parts[idx]} kişi', lot_count, budget]
    
    return df

def calc_lot_budget_page():
    starting_price = st.number_input('Başlangıç fiyatını giriniz.', value=10.0, step=0.2)
    number_of_lots = st.number_input('Toplam lot sayısını giriniz.', value=5000000, step=50000)

    df = calculate_lot_count_and_budget(starting_price, number_of_lots)

    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={'number_of_participants': 'Katılımcı Sayısı',
                                'lot_count': 'Lot Sayısı',
                                'budget': 'Bütçe'}
                                )

def calc_profit_page():
    initial_price = st.number_input('Başlangıç fiyatı', value=10.0, step=0.2)
    lot_count = st.number_input('Lot miktarı', value=10, step=1)
    days = st.number_input('Gün sayısı', value=10, step=1)

    df = simulate_trades(days, initial_price, lot_count)

    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={'tavan_sayisi': 'Tavan Sayısı',
                                'tavan_fiyati': 'Tavan Fiyatı',
                                'gunluk_kar': st.column_config.NumberColumn(
                                    'Günlük Kar', format= '%.2f ₺'),
                                'toplam_kar': st.column_config.NumberColumn(
                                    'Toplam Kar', format= '%.2f ₺'),
                                'toplam_kar_yuzdesi': st.column_config.NumberColumn(
                                    'Toplam Kar Yüzdesi', format= '%.2f %%')}
                                )


def main():
    st.title('Halka Arz Tavan Uygulaması')

    img = Image.open("halka_arz_logo.png").resize((800, 300))
    with st.columns(3)[1]:
        st.image(img)

    st.markdown('''
    Bu uygulama, halka arz hisse senedi alım-satımında tavan uygulamasının karlılığını göstermektedir.
    ''')

    tab1, tab2 = st.tabs(['Kar Hesapla', 'Lot ve Bütçe Hesapla'])
    with tab1:
        calc_profit_page()
    with tab2:
        calc_lot_budget_page()

if __name__ == "__main__":
    main()
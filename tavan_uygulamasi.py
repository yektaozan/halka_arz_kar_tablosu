import numpy as np
import pandas as pd
import warnings
import streamlit as st
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

def add_ceiling(x):
    return x * 1.1

def daily_profit(current_price, previous_price, lot_count):
    return (current_price - previous_price) * lot_count

def total_profit(current_price, initial_price, lot_count):
    return (current_price - initial_price) * lot_count

def simulate_trades(days, initial_price, lot_count):
    df = pd.DataFrame(columns=['tavan_sayisi', 'tavan_fiyati', 'gunluk_kar', 'toplam_kar'])
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

        df.loc[len(df.index)] = [i+1, current_price, daily_profit_value, total_profit_value]

    return df

def main():
    st.title('Halka Arz Tavan Uygulaması')
    st.markdown('''
    Bu uygulama, halka arz hisse senedi alım-satımında tavan uygulamasının karlılığını göstermektedir.
    ''')

    initial_price = st.number_input('Başlangıç fiyatı', value=10.0, step=0.01)
    lot_count = st.number_input('Lot miktarı', value=10, step=1)
    days = st.number_input('Gün sayısı', value=10, step=1)

    df = simulate_trades(days, initial_price, lot_count)

    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={'tavan_sayisi': 'Tavan Sayısı',
                                'tavan_fiyati': 'Tavan Fiyatı',
                                'gunluk_kar': st.column_config.NumberColumn(
                                    'Günlük Kar', format= '%.2f ₺'),
                                'toplam_kar': st.column_config.NumberColumn(
                                    'Toplam Kar', format= '%.2f ₺')}
                                )

if __name__ == '__main__':
    main()


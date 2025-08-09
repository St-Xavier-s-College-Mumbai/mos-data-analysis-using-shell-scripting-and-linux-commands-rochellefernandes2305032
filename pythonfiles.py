import pandas as pd
import matplotlib.pyplot as plt

#SHIPPING MODE DISTRIBUTION
df = pd.read_csv('cleaned_data.csv')
ship_mode_series = df.iloc[:, 4]
ship_mode_counts = ship_mode_series.value_counts()
color_map = {
    'First Class': '#1f77b4',    
    'Second Class': '#66b3ff',   
    'Standard Class': '#99ccff',  
    'Same Day': '#3399cc'        
}
colors = [color_map.get(mode, '#cccccc') for mode in ship_mode_counts.index]
plt.figure(figsize=(8, 8))
plt.pie(
    ship_mode_counts,
    labels=ship_mode_counts.index,
    colors=colors,
    autopct='%1.1f%%',
    startangle=140,
    shadow=True
)
plt.title('Shipping Mode Distribution', pad=30)
plt.axis('equal')  # Keep circle shape
plt.tight_layout()
plt.savefig('shipping_mode_pie.png')


#TOP 10 STATES BY PROFIT AND ORDER COUNT
df = pd.read_csv("cleaned_data.csv", header=None)
df_subset = df.iloc[:, [10, 20]]
df_subset.columns = ['State', 'Profit']
state_summary = df_subset.groupby('State').agg(
    Total_Profit=('Profit', 'sum'),
    Order_Count=('Profit', 'count')
).reset_index()
top_states = state_summary.sort_values(by='Total_Profit', ascending=False).head(10)
plt.figure(figsize=(12, 6))
bars = plt.barh(top_states['State'], top_states['Total_Profit'], color='skyblue')
for i, (profit, count) in enumerate(zip(top_states['Total_Profit'], top_states['Order_Count'])):
    label = f"₹{profit:,.0f} (Count: {count})"
    plt.text(profit + 100, i, label, va='center', fontsize=9)
plt.xlabel("Total Profit")
plt.title("Top 10 States by Profit with Order Count")
plt.gca().invert_yaxis()  
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("top_10_states_with_profit_and_count.png")
plt.show()


#TOP 5 CITIES WITH HIGH DISCOUNTS
df = pd.read_csv('cleaned_data.csv', header=None)
df_clean = df[[9, 19]].dropna()
df_clean.columns = ['City', 'Discount']
total_counts = df_clean['City'].value_counts()
high_counts = df_clean[df_clean['Discount'] > 0.5]['City'].value_counts()
combined = pd.DataFrame({'Total': total_counts, '>50%': high_counts}).fillna(0)
combined_sorted = combined.sort_values(by='>50%', ascending=False)
top5 = combined_sorted.head(5)
fig, ax = plt.subplots(figsize=(12, 7))
bar_width = 0.35
x = range(len(top5))
bars1 = ax.bar(x, top5['Total'], width=bar_width, label='Total Discounts', color='midnightblue')
bars2 = ax.bar([i + bar_width for i in x], top5['>50%'], width=bar_width, label='>50% Discounts', color='skyblue')
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(top5.index, rotation=45, ha='right')
ax.set_ylabel('Count')
ax.set_title('Top 5 Cities with Most Discounts (>50%)')
ax.legend()
for i, (total, high) in enumerate(zip(top5['Total'], top5['>50%'])):
    ax.text(i, total + 5, int(total), ha='center', fontsize=9, color='black')
    ax.text(i + bar_width, high + 5, int(high), ha='center', fontsize=9, color='black')

plt.tight_layout()
plt.savefig('sorted_top5_discounts.png')
plt.show()


#MONTHLY ORDER VOLUME 2020
df = pd.read_csv('cleaned_data.csv', header=None)
df[2] = pd.to_datetime(df[2], errors='coerce', dayfirst=True)
df_2020 = df[df[2].dt.year == 2020].copy()
df_2020['Month'] = df_2020[2].dt.strftime('%b')
df_2020['Month_Num'] = df_2020[2].dt.month
monthly_orders = df_2020.groupby(['Month_Num', 'Month']).size().reset_index(name='OrderCount')
monthly_orders = monthly_orders.sort_values('Month_Num')
plt.figure(figsize=(11, 7))
plt.plot(monthly_orders['Month'], monthly_orders['OrderCount'], marker='o', linestyle='-', color='mediumblue')
for i, txt in enumerate(monthly_orders['OrderCount']):
    plt.annotate(txt,
                 (monthly_orders['Month'].iloc[i], monthly_orders['OrderCount'].iloc[i] + 19),
                 ha='center',
                 fontsize=8,
                 color='black')
plt.ylim(0,400)
plt.title('Monthly Order Volume (2020)', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('monthly_order_volume_2020_adjusted.png', dpi=300)
plt.show()



#AVERAGE DELIVERY TIME BY SHIPPING MODE
file_path = 'cleaned_data.csv' 
df = pd.read_csv(file_path, header=None)
order_date_col = 2
ship_date_col = 3
ship_mode_col = 4
df[order_date_col] = pd.to_datetime(df[order_date_col], dayfirst=True, errors='coerce')
df[ship_date_col] = pd.to_datetime(df[ship_date_col], dayfirst=True, errors='coerce')
df['DeliveryTime'] = (df[ship_date_col] - df[order_date_col]).dt.days
df = df.dropna(subset=['DeliveryTime'])
df = df[df['DeliveryTime'] >= 0]
avg_delivery = df.groupby(ship_mode_col)['DeliveryTime'].mean()
order_counts = df[ship_mode_col].value_counts()
summary_df = pd.DataFrame({
    'AvgDeliveryTime': avg_delivery,
    'OrderCount': order_counts
}).dropna().sort_values(by='AvgDeliveryTime')
plt.figure(figsize=(12, 6))
bars = plt.bar(
    summary_df.index,
    summary_df['AvgDeliveryTime'],
    color='#191970'  # Midnight Blue
)
for bar, count, avg in zip(bars, summary_df['OrderCount'], summary_df['AvgDeliveryTime']):
    height = bar.get_height()
    visible_height = height if height > 0.1 else 0.1 
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        visible_height + 0.1,
        f'{int(count)} orders\n{avg:.1f} days',
        ha='center',
        va='bottom',
        fontsize=9,
        color='black'
    )
plt.title('Average Delivery Time by Shipping Mode', fontsize=14)
plt.xlabel('Shipping Mode')
plt.ylabel('Avg Delivery Time (Days)')
plt.ylim(0, max(summary_df['AvgDeliveryTime']) + 1)  # Adjust Y limit
plt.tight_layout()
plt.savefig('/home/rochelle/Downloads/shipping_mode_chart.png')
plt.show()


#CATEGORY BY SALES SHARE
df = pd.read_csv('/home/rochelle/Downloads/cleaned_data.csv', header=None)
df = df[[14, 18]].dropna()
df[18] = pd.to_numeric(df[18], errors='coerce')
top_sales = df.groupby(14)[18].sum().sort_values(ascending=False).head(10)
colors = plt.cm.Blues_r(range(40, 255, 22))
plt.figure(figsize=(8, 8))
plt.pie(top_sales.values, labels=top_sales.index, autopct='%1.1f%%',
        startangle=140, colors=colors[:len(top_sales)])
plt.title('Category by Sales Share ', fontsize=14)
plt.tight_layout()
plt.savefig("salespro.png")
plt.show()


#TOP 10 ACTIVE CUSTOMERS BY NUMBER OF ORDERS
df = pd.read_csv("cleaned_data.csv", header=None)
order_counts = df[6].value_counts().head(10)
plt.figure(figsize=(15,7))
bars = plt.bar(order_counts.index, order_counts.values, color='midnightblue')
plt.title("Top 10 Most Active Customers (by Number of Orders)", fontsize=14, pad=20)
plt.xlabel("Customer Names", fontsize=12)
plt.ylabel("Number of Orders", fontsize=12)
plt.xticks(rotation=45, ha='right')
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1, str(height),
             ha='center', va='bottom', fontsize=9)
plt.ylim(0, 45)
plt.tight_layout()
plt.savefig("active.png")
plt.show()


#Region-wise number of orders
cut -d',' -f13 cleaned_data.csv | sort | uniq -c | sort -nr > region_counts.dat
set terminal pngcairo size 800,600 enhanced font 'Verdana,10'
set output 'region_orders.png'
set title 'Region-wise Number of Orders'
set xlabel 'Region'
set ylabel 'Number of Orders'
set style data histograms
set style fill solid 1.0 border -1
set boxwidth 0.5
set grid ytics
set key off
set style line 1 lc rgb "#191970" lt 1 lw 2
plot 'region_counts.dat' using 1:xtic(2) with boxes ls 1, \
     '' using 0:1:1 with labels offset 0,1 notitle

#YEARLY GROWTH
cut -d',' -f4 cleaned_data.csv | head
cut -d',' -f4 cleaned_data.csv | cut -d'/' -f3 | sort | uniq -c > yearly_orders.txt
set terminal png size 800,600
set output 'yearly_growth.png'
set title "Year-over-Year Order Volume"
set xlabel "Year"
set ylabel "Number of Orders"
set grid
set style line 1 lc rgb "#003366" lw 2 pt 7 ps 1.5
plot 'yearly_orders.txt' using 2:1 with linespoints ls 1 title 'Orders'


#TOP 5 SUB CATEGORIES SOLD
cut -d',' -f16 cleaned_data.csv | sort | uniq -c | sort -nr | head -5 > subcategory_counts.dat
set terminal pngcairo size 800,600 enhanced font 'Verdana,10'
set output 'top_subcategories.png'
set title 'Top 5 Sub-Categories Sold'
set xlabel 'Sub-Category'
set ylabel 'Number of Orders'
set style data histograms
set style fill solid 1.0 border -1
set boxwidth 0.5
set grid ytics
set key off
set style line 1 lc rgb "#191970" lt 1 lw 2
plot 'subcategory_counts.dat' using 1:xtic(2) with boxes ls 1, \
     '' using 0:1:1 with labels offset 0,1 notitle


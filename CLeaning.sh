#DATA PREPROCESSING STEPS
#1 View the first few lines
head -n 5 data.csv
#2. Check for missing data
awk -F',' '{ for(i=1;i<=NF;i++) if($i=="") print "Missing in line", NR }' data.csv
#3. Remove rows with missing essential fields
awk -F',' 'NF==6 && $4!="" && $6!=""' data.csv > cleaned_step1.csv
#4. Strip special characters from numeric columns
sed 's/₹//g; s/%//g; s/,//g' cleaned_step1.csv > cleaned_data.csv

#Installation
Sudo apt install gnuplot
sudo apt install python3-pip
sudo apt install python3-venv -y       
python3 -m venv myenv                 
source myenv/bin/activate              
pip install matplotlib                
pip install squarify matplotlib pandas
pip install plotly


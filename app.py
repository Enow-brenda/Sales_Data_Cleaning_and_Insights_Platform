'''
Algorithm approach is to create an array that will hold the data and then clean it before creating it and then creating another file with that data
''' 
import csv
from flask import Flask,request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def get_clean_data():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename and file.filename.split(".")[-1]=="csv":
          fileName=open_file_and_work(file)
          try:
            with open(fileName,mode='r') as file:
              csv_file = csv.reader(file.read().splitlines()) 
              csv_file = list(csv_file)
              return jsonify(csv_file)
          except FileNotFoundError:
              return "Error: The file was not found."
          except PermissionError:
              return "Error: You do not have permission to access this file."
          except Exception as e:
              return f"An unexpected error occurred: {e}"
        else:
          return "Can only process csv files"
    else:
      return "Unexpected Error Happened"

@app.route("/getOtherData", methods=['GET'])
def get_other_data():
    if request.method == 'POST':
        data=open_any_file(request.args['filename'])
        highest_sales=products_with_highest_sales(data)
        product_more_500=products_with_more_than_500_unit_sold(data)
        average=average_price(data)
        output="Names of Products with Highest Sales of "+str(highest_sales[0][2])+" are :\n"
        count=0
        for product in highest_sales:
         output=output+str(count+1)+". "+product[1]+" - "+product[2]+"\n";
        count==0
        output=output+"\nNames of Products with more than 500 unit sold are :\n"
        for product in product_more_500:
          output=output+str(count+1)+". "+product[1]+" - "+product[2]+"\n";
        output=output+"Average Price of all Products is : "+str(average)
        return output
    else:
      return "Unexpected Error Happened"
        
        

def clean_data(products):
  new_data=[]
  #clean the data
  for product in products:
    return_value=remove_fields(product)
    if return_value!=0:
      new_data.append(return_value)

  #calculating the total sales each product
  for product in new_data:  
    product[4]=float(product[2])*float(product[3])
  return new_data

def remove_fields(product):
  critical_data_index=[0,1,2,3];
  sales_data_index=[2,3,4];

  for i in critical_data_index:
    if product[i]=="":
      return 0
  for i in sales_data_index:
    if float(product[i])<0:
      return 0
  if float(product[2])==0 or float(product[3])>1000:
    return 0
  return product

def get_highest_sales(products):
  highest_sales=0
  for product in products:
    if float(product[3])>highest_sales:
      highest_sales=float(product[3])
  return highest_sales

def products_with_highest_sales(products):
  highest_sales=get_highest_sales(products)
  highest_products=[];
  for product in products:
    if float(product[4])==highest_sales:
      highest_products.append(product)
  return highest_products

def products_with_more_than_500_unit_sold(products):
  higher_unit_products=[];
  for product in products:
    if float(product[3])>500:
      higher_unit_products.append(product)
  return higher_unit_products

def average_price(products):
  total_price=0
  count=0
  for product in products:
    total_price=total_price+float(product[2])
    count=count+1
  return total_price/count

#creating a new clean file
def create_new_file(new_data,file_name):
  new_name="cleaned_files/new_"+file_name
  with open(new_name,mode="w") as file:
    writer=csv.writer(file)
    writer.writerows(new_data)
  return new_name

def open_file_and_work(file):
  datas = []
  try:
    with open(file,mode='r') as file:
      csv_file = csv.reader(file.read().splitlines())
      header = next(csv_file)  # Get the header
      for product in csv_file:
        datas.append(product)
      cleaned_data=clean_data(datas)
    #adding the headers to create a new csv file
      cleaned_data.insert(0,header)
      new_filename=create_new_file(cleaned_data,file)
      return new_filename
  except FileNotFoundError:
      return "Error: The file was not found."
  except PermissionError:
      return "Error: You do not have permission to access this file."
  except Exception as e:
      return f"An unexpected error occurred: {e}"

def open_any_file(file):
  try:
    with open(file,mode='r') as file:
      csv_file = csv.reader(file.read().splitlines())
      header = next(csv_file)  
      return csv_file
  except FileNotFoundError:
      return "Error: The file was not found."
  except PermissionError:
      return "Error: You do not have permission to access this file."
  except Exception as e:
      return f"An unexpected error occurred: {e}"


if __name__ == '__main__':
  app.run(debug=True)












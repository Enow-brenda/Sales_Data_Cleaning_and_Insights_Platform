'''
Algorithm approach is to create an array that will hold the data and then clean it before creating it and then creating another file with that data
''' 
import csv

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
  
def open_file_and_work(file_name):
  datas = []
  try:
    with open(file_name,mode='r') as file:
      csv_reader=csv.reader(file)
      header=next(csv_reader)

      for product in csv_reader:
        datas.append(product)
    cleaned_data=clean_data(datas)
    #adding the headers to create a new csv file
    cleaned_data.insert(0,header)
    new_filename=create_new_file(cleaned_data,file_name)
    return new_filename
  except FileNotFoundError:
      return "Error: The file was not found."
  except PermissionError:
      return "Error: You do not have permission to access this file."
  except Exception as e:
      return f"An unexpected error occurred: {e}"
  
    

file_name="product_sales_50_records.csv"
extension=file_name.split(".")[-1]
if(extension=="csv"):
  output=open_file_and_work(file_name)
  print(output)
else:
  print("Can only process csv files")







  


  
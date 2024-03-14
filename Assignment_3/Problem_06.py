box1=""
box2=""
box3=""

lab1=""
lab2=""
lab3=""

negation1=""
negation2=""
negation3=""

if __name__=="__main__":
    input_labels = input("Enter the labels in the form of three letter strings\nFor example if the labels are White Yellow and Both respectively enter WYB : \t")
    negation1 = input_labels[0]
    negation2 = input_labels[1]
    negation3 = input_labels[2]

    lab1 = input_labels[0]
    lab2 = input_labels[1]
    lab3 = input_labels[2]

    input_contents = input("Enter the contents in the form of three letter strings\nFor example if the contents are White Yellow and White respectively enter WYW : \t")
    
    box1=input_contents[0]
    box2=input_contents[1]
    box3=input_contents[2]

    if(lab1 == negation1):
      print(f"Box 1 is incorrectly labelled hence it cannot contain be {negation1}\n")
      lab1, lab2 = input_labels[1], input_labels[0]
      if(lab1 == "W" AND box1 == "Y"):
         lab1, lab3 = input_labels[0], input_labels[2]
          
      

import pickle


string = "à, è, ì, ò, ù,"
print(string)
f=open("save.pkl","wb")
pickle.dump(string,f)
f.close()
newstring = pickle.load(open("save.pkl","rb"))
print(newstring)
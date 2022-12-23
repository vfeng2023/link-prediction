"""
Gets the valid nodes -- dumps content in text files into a pickle file
"""
import pickle
filenames = [
    "Characters_in_The_Hobbit.txt",
    "Characters_in_The_Lord_of_the_Rings.txt",
    "Characters_in_The_Silmarillion.txt",
    "Locations.txt"
]

valid_characters = set()
for f in filenames:
    with open(f,'r') as fle:
        lines = fle.readlines()
        for line in lines:
            line = line.strip()
            valid_characters.add(line)

# save this 

print(valid_characters)
print(len(valid_characters))
save_file = open('allowed_names.pkl','wb')
pickle.dump(valid_characters,save_file)
print("saved!")

import random
import string

length = 15
characters = string.ascii_letters + string.digits + string.punctuation
password = ''.join(random.choice(characters) for _ in range(length)) 

print("Generated Password:", password)


name = input("Lucifer")
age = 80

future_age = age + 5

print("Hello", name)
print("In 5 years you will be", future_age, "years old")

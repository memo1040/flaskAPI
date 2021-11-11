# print your Name
print("Guillermo Monge")

# print a range of numbers
l = 30
u = 70
for num in range(l, u + 1):
    print(num)

# count the number of lines in a text file
file = open("notes.txt", "r")
line_count = 0
for line in file:
    if line !="\n":
        line_count += 1
file.close()

print(f"You have {line_count} lines")

## alternate
file = open("notes.txt", "r")
lines = file.readlines()
print(f"You have {len(lines)} lines")
file.close()

# create a new file
file = open("demo.txt", "w")
file.write("Hello from python\n")
file.write("This should be a second line\n")
file.close()

# write a line at the bottom of a text file
file = open("notes.txt", "a")
file.write("\nThis is the notes file")
file.close()
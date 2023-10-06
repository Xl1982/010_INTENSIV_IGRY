import calculator
num1 = float(input("Введите первое число: "))
num2 = float(input("Введите второе число: "))

print("Выберите операцию:")
print("1. Сложение")
print("2. Вычитание")
print("3. Умножение")
print("4. Деление")

choice = int(input("Введите номер выбранной операции: "))

if choice == 1:
    print(num1, "+", num2, "=", calculator.add(num1, num2))

elif choice == 2:
    print(num1, "-", num2, "=", calculator.subtract(num1, num2))

elif choice == 3:
    print(num1, "*", num2, "=", calculator.multiply(num1, num2))

elif choice == 4:
    print(num1, "/", num2, "=", calculator.divide(num1, num2))

else:
    print("Недопустимый выбор.")
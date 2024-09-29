import re
import pwinput

f = open('rasrabotka/данные.txt', 'r')
file = f.readlines()
logs = []
mails = []
tele = []
count = 0
for i in f:
    logs.append(file[count].split()[0])
    mails.append(file[count].split()[2])
    tele.append(file[count].split()[3])
    count += 1
f.close()

nachalo = input('Выберете войти в систему или зарегистрироваться: ')
if nachalo == 'вход':
    login = input('Введите логин: ')
      c = 0
    for i in file:
        i = [x for x in file[c].split()]
        if login == i[0]:
            print(f'Логин: {i[0]}\nПароль: {i[1]}\nЭлектронная почта: {i[2]}\nТелефон: {i[3]}\nФИО: {i[4]}\nГород: {i[5]}\nО себе: {i[6]}')
            break
        else:
            c += 1
   
if nachalo == 'регистрация':
    login = input('Введите логин: ')
    while len(login) < 5:
        login = input('Логин слишком короткий, повторите ввод: ')
    while re.search(r'[^a-zA-Z0-9]', login):
        login = input('Логин должен состоять только из латинских букв и цифр, повторите ввод: ')
    while login in logs:
        login = input('Данный логин уже существует, повторите ввод: ')

    password = pwinput.pwinput(prompt='Создайте пароль: ')
    while True:
        if password.lower == password:
            password = pwinput.pwinput(prompt='В пароле должна быть хотя бы одна заглавная буква, повторите ввод: ')
        elif password.upper == password:
            password = pwinput.pwinput(prompt='В пароле должна быть хотя бы одна строчная буква, повторите ввод: ')
        elif len(password) < 8:
            password = pwinput.pwinput(prompt='Пароль слишком короткий, повторите ввод: ')
        elif any(ch.isdigit() for ch in password) == False:
            password = pwinput.pwinput(prompt='В пароле должна быть хотя бы одна цифра, повторите ввод: ')
        elif set('.,^$;!-_@#()[]{}%&*').isdisjoint(password):
            password = pwinput.pwinput(prompt='В пароле должен быть хотя бы один специальный символ, повторите ввод: ')
        else:
            paspov = pwinput.pwinput(prompt='Повторите пароль: ')
            if paspov != password:
                password = pwinput.pwinput(prompt='Повтор не соответствует исходному паролю, введите пароль заново: ')
                paspov = ''
            if paspov == password:
                break
    mail = input('Введите электронную почту: ')
    while '@' not in mail:
        mail = input('В почте должен быть один знак @, повторите ввод: ')
    while mail[0] == '@':
        mail = input('Почта не должна начинаться со знака @, повторите ввод: ')
    while mail[-1] == '@':
        mail = input('Почта не должна заканчиваться знаком @, повторите ввод: ')
    while mail.count('@') > 1:
        mail = input('В почте должен быть один знак @, повторите ввод: ')
    if mail in mails:
        print('На данную почту уже зарегистрирован аккаунт.')

    tsifr = '0123456789'
    nomer = input('Введите номер телефона: ')
    flag_nomer = True
    nomer = nomer.replace(' ', '')
    telephone = nomer
    if nomer[0] == '+':
        if nomer[1] != '7':
            flag_nomer = False
        nomer = nomer.replace('+', '')
    if nomer[0] not in '78':
        flag_nomer = False
    for i in range(len(nomer)):
        if nomer[i] not in tsifr:
            flag_nomer = False
    if flag_nomer == True and len(nomer) != 11:
        flag_nomer = False
    while flag_nomer == False:
        nomer = input('Номер введён не верно, повторите ввод: ')
        nomer = nomer.replace(' ', '')
        telephone = nomer
        flag_nomer = True
    if telephone in tele:
        print('На данный номер уже зарегистрирован аккаунт.')

    print('Дополнительные поля, заполнять не обязательно.')
    fio = input('Введите ФИО: ')
    if fio == '':
        fio = '-'
    city = input('Введите город: ')
    if city == '':
        city = '-'
    o_sebe = input('О себе: ')
    if o_sebe == '':
        o_sebe = '-'

    with open("rasrabotka/данные.txt", "a") as f:
        f.write(login + ' ' + password + ' ' + mail + ' ' + telephone + ' ' + fio + ' ' + city + ' ' + o_sebe + '\n')

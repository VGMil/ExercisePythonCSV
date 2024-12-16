import pandas as pd

cuestionarioCSV = "./CIIC2024/CIIC2024_cuestionario.csv"
cols_cuestionarioCSV = [1,2]
inscritos_camaraCSV = "./CIIC2024/CIIC2024_inscritos_cámara.csv"
inscritos_departamentoCSV = "./CIIC2024/CIIC2024_inscritos_dapartamento.csv"
registro_asistenciaCSV = "./CIIC2024/CIIC2024_regitro_asistencia.csv"

def menu():
    print("1. ¿Cuál fue el número de inscritos en el congreso?")
    print("2. ¿Cuál fue el número de personas que asistieron sólo un día al congreso?")
    print("3. ¿Cuál fue el número de personas que asistieron sólo dos días al congreso?")
    print("4. ¿Cuál fue el número de personas que asistieron los tres días del congreso?")
    print("5. Lista de las personas que asistieron el primer día del congreso")
    print("6. Lista de las personas que asistieron el segundo día del congreso")
    print("7. Lista de las personas que asistieron el tercer día del congreso")
    print("8. Lista de las personas que asistieron solamente dos días al congreso")
    print("9. Lista de las personas que asistieron los tres días del congreso")
    print("10. Lista de las personas que tienen certificado de aprobación")
    print("0. Salir")
def read_csv_cuestionario(file_path,cols):
    df = pd.read_csv(file_path, usecols=cols)
    return df
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df
def getListforDay(registro_asistencia, inscritos, date_asistencia):
    date = pd.to_datetime(date_asistencia, dayfirst=True).date()
    registroday = registro_asistencia[registro_asistencia["Marca temporal"]==date]
    inscritos_day = inscritos[inscritos["Documento de identidad"].isin(registroday["Documento de identidad"])]
    return inscritos_day

def getListforDays(assists, inscritos, quantity):
    registrodays = assists[assists["count"]==quantity]
    inscritos_days = inscritos[inscritos["Documento de identidad"].isin(registrodays["Documento de identidad"])]
    return inscritos_days
    

def getListApproved(assists, cuestionario, inscritos):
    evaluated = pd.merge(assists, cuestionario, on="Documento de identidad")
    approved = evaluated[(evaluated["count"] >= 2) &( evaluated["Puntuación"] >= 7)]
    inscritos_approved = inscritos[inscritos["Documento de identidad"].isin(approved["Documento de identidad"])]
    return inscritos_approved

def main():
    cuestionario = read_csv_cuestionario(cuestionarioCSV, cols_cuestionarioCSV)
    cuestionario["Puntuación"] = cuestionario["Puntuación"].str.split('/').str[0].astype(int) #review
    inscritos_camara = read_csv(inscritos_camaraCSV)
    inscritos_departamento = read_csv(inscritos_departamentoCSV)

    registro_asistencia = read_csv(registro_asistenciaCSV)
    registro_asistencia["Marca temporal"] = pd.to_datetime(registro_asistencia["Marca temporal"], dayfirst=True).dt.date
    registro_asistencia = registro_asistencia.drop_duplicates(subset=["Marca temporal", "Documento de identidad"])
    
    assists = registro_asistencia["Documento de identidad"].value_counts().reset_index()
    
    inscritos = pd.concat([inscritos_camara, inscritos_departamento])
    inscritos["Nombres"] = inscritos["Nombres"].str.capitalize()
    inscritos = inscritos.drop_duplicates()
    
    resultado = 0
    while(True):
        menu()
        opcion = int(input("Ingrese Opcion -> "))
        match opcion:
            case 0:
                print("Gracias por Revisar")
                break
            case 1:
                resultado = inscritos
                print("En total tenemos " + str(len(inscritos)) + " inscritos")
            case 2:
                resultado = getListforDays(assists,inscritos, 1)
                print("En total  asistieron: "+ str(len(resultado)))
                print("Profesionales: "+ str(len(resultado[(resultado["Oficio"] =="Profesional")])))
                print("Estudiantes: "+ str(len(resultado[(resultado["Oficio"] =="Estudiante")])))
                print("Otros roles:" + str(len(resultado[(resultado["Oficio"] != "Profesional") & (resultado["Oficio"] != "Estudiante")])))
            case 3:
                resultado = getListforDays(assists,inscritos, 2)
                print("En total  asistieron: "+ resultado.sum())
                print("En total  asistieron: "+ str(len(resultado)))
                print("Profesionales: "+ str(len(resultado[(resultado["Oficio"] =="Profesional")])))
                print("Estudiantes: "+ str(len(resultado[(resultado["Oficio"] =="Estudiante")])))
                print("Otros roles:" + str(len(resultado[(resultado["Oficio"] != "Profesional") & (resultado["Oficio"] != "Estudiante")])))
            case 4:
                resultado = getListforDays(assists,inscritos, 3)
                print("En total  asistieron: "+ str(len(resultado)))
                print("Profesionales: "+ str(len(resultado[(resultado["Oficio"] =="Profesional")])))
                print("Estudiantes: "+ str(len(resultado[(resultado["Oficio"] =="Estudiante")])))
                print("Otros roles:" + str(len(resultado[(resultado["Oficio"] != "Profesional") & (resultado["Oficio"] != "Estudiante")])))
            case 5:
                aux = getListforDay(registro_asistencia, inscritos, "2024-11-27")
                resultado = "Asistieron el dia 27 de noviembre del 2024 \n"+ aux["Nombres"] +": "+ aux["Oficio"]
            case 6:
                aux = getListforDay(registro_asistencia, inscritos, "2024-11-28")
                resultado = "Asistieron el dia 28 de noviembre del 2024 \n"+ aux["Nombres"] +": "+ aux["Oficio"]
            case 7:
                aux = getListforDay(registro_asistencia, inscritos, "2024-11-29")
                resultado = "Asistieron el dia 29 de noviembre del 2024 \n"+ aux["Nombres"] +": "+ aux["Oficio"]
            case 8:
                aux = getListforDays(assists, inscritos, 2)
                resultado = "Asistieron 3 dias \n"+ aux["Nombres"] +": "+ aux["Oficio"]
            case 9:
                aux = getListforDays(assists, inscritos, 3)
                resultado = "Asistieron 3 dias \n" + aux["Nombres"] +": "+ aux["Oficio"]
            case 10:
                aux = getListApproved(assists, cuestionario, inscritos)
                resultado = "Aprobado "+ aux["Nombres"] +": "+ aux["Oficio"]
        print(resultado)    
    
        input("Presione ENTER para continuar")



main()

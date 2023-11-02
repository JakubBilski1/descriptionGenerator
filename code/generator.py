import openai
import json

openai.api_key = 'YOUR TOKEN'

def getProductsArray():
    with open('products.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    products = [line.strip() for line in lines]
    return products

def getMachinesArray():
    with open('machines.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    machines = [line.strip() for line in lines]
    return machines

ending = "Wymianę części zamiennych warto powierzyć profesjonalistom. Podczas przeglądu przeprowadzonego przez doświadczonego mechanika można wykryć drobne usterki, które, jeśli zaniedbane, mogą prowadzić do poważnych awarii. Ważne jest również, aby wszystkie części do maszyn budowlanych pochodziły z pewnego i zaufanego źródła. W naszym sklepie oferujemy szeroki wybór wysokiej jakości części zamiennych do maszyn znanych, a także cenionych producentów. Takich jak CASE CONSTRUCTION, NEW HOLLAND, TEREX, YANMAR i SCHAEFF. Nasze filtry można nabyć zarówno jako pojedyncze egzemplarze, jak i w wygodnych zestawach. Serdecznie zapraszamy do zapoznania się z naszą ofertą."

def getDescription(product, machine):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"opisz mi {product} do {machine}, bez używania strony biernej w minimum 350 słowach"},
        ]
    )
    def getEndingTitle():
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"daj mi tylko i wyłącznie jeden tytuł podobny do 'dlaczego warto postawić na nas', ma być on inny niż tytuł w stylu '10 powodów dla których...'"},
            ]
        )
        return completion.choices[0].message.content
    def getMiddleTitle(description):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Podaj mi tylko i wyłącznie tytuł, który opisuje ten opis: {description}"},
            ]
        )
        return completion.choices[0].message.content
    descript = completion.choices[0].message.content
    formattedDescript = descript.replace("\n", "")
    answer = {
        "title": product,
        "desc": formattedDescript,
        "middleTitle": getMiddleTitle(formattedDescript),
        "endingTitle": getEndingTitle(),
        "ending": ending
    }
    return answer

output_file_name = "opisyTest.json"
descriptions = []

for i, (prod, machine) in enumerate(zip(getProductsArray(), getMachinesArray())):
    description = getDescription(prod, machine)
    descriptions.append(description)
    print(f"Added description number {i+1}...")

with open(output_file_name, 'w', encoding='utf-8') as output_file:
    json.dump(descriptions, output_file, indent=4, ensure_ascii=False)

print(f"Descriptions appended to {output_file_name}")
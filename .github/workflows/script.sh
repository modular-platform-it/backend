author=sihuannewrise
echo ${team[$author]}
declare -A ids=([geroy4ik]=1525888085 [olees-orlenko]=423285129 [sihuannewrise]=228559330 [paymir121]=462624293)
declare -A nicks=([geroy4ik]=geroy4ik [olees-orlenko]=olees [sihuannewrise]=sihuan [paymir121]=nikiromanov)

# возврат ключей на разных строках
for key in "${!team[@]}"; do echo $key; done
# в одну строку
echo ${!team[@]}

# возврат значений на разных строках
for key in "${team[@]}"; do echo $key; done
# в одну строку
echo ${team[@]}

# вывод ключ-значение
for key in ${!team[@]}; do echo "$key - ${team[$key]}"; done
# кол-во ключей в словаре
echo ${#team[@]}

# проверить наличие элемента массива с помощью оператора «+_»
if [ ${team[olees-orlenko]+_} ]; then echo "Found"; else echo "Not found"; fi
if [ ${team[sihuannewrise]+_} ]; then echo 1; else echo 0; fi
if [ ${team[$author]+_} ]; then echo 1; else echo 0; fi

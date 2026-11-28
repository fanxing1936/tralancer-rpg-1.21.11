# 每刻记下血量（×10），挨了不该挨的打时补回去
execute as @a store result score @s rpg_pv_hp run data get entity @s Health 10

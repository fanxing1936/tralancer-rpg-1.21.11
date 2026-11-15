# overcharge 第 17 刻的姿势（每 1 刻一帧，补间 1 刻）。由 add_prime_enchanter_model.py 烘焙。
data modify storage rpg:prime_enchanter pose set value {}
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.prime_enchanter.part] run function rpg:prime_enchanter/anim/apply with entity @s item.components."minecraft:custom_data"

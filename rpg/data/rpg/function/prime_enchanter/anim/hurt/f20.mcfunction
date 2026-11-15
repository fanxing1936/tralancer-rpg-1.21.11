# hurt 第 20 刻的姿势（每 1 刻一帧，补间 1 刻）。由 add_prime_enchanter_model.py 烘焙。
data modify storage rpg:prime_enchanter pose set value {"hat_ribbons":{translation:[-0.05645f,0.11209f,-1.27127f],left_rotation:[0.24891f,-0.02153f,0.02404f,0.96799f],scale:[1.15f,1.15f,1.15f],right_rotation:[0f,0f,0f,1f]}}
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.prime_enchanter.part] run function rpg:prime_enchanter/anim/apply with entity @s item.components."minecraft:custom_data"

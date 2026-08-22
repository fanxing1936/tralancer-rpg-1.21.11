advancement revoke @s only rpg:item/power
execute at @s[nbt={Inventory:[{Slot:-106b,components:{"minecraft:custom_data":{power_tag:1b}}}]}] run particle enchant ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20


execute at @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run scoreboard players add @s power_step 1
execute at @s[nbt={SelectedItem:{components:{"minecraft:custom_data":{power_tag:1b}}}}] run particle enchant ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20


tag @s remove rpg.usb.exposed
execute on passengers if entity @s[tag=rpg.prime_enchanter.p.head] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if entity @s[tag=rpg.usb.reauth] run tag @s add rpg.usb.auth
tag @s remove rpg.usb.reauth

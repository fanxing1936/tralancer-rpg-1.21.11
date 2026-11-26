scoreboard players set #b rpg_fo 0
execute if entity @s[tag=rpg.pope] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.mkb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.jqb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.lub] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.slb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.usb] run scoreboard players set #b rpg_fo 1
execute if entity @s[tag=rpg.dtb] run scoreboard players set #b rpg_fo 1
execute unless score #b rpg_fo matches 1 run return 0
scoreboard players operation #d rpg_fo *= #105 rpg_fo
scoreboard players operation #d rpg_fo /= #100 rpg_fo

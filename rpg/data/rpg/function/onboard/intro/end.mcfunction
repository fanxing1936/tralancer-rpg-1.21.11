# 旁白放完或跳过：到欢迎页起名
function rpg:onboard/intro/stop
scoreboard players set @s rpg_ob 2
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 0.6 0.7
function rpg:onboard/show

# 买断。它不掷点 —— 贪婪不赊账，这一箭的价钱是写死的。
function rpg:hud/m22
playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.8
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 0.6
execute at @s anchored eyes run particle wax_on ^ ^ ^1 0.3 0.3 0.3 0.1 40
execute at @s anchored eyes run particle end_rod ^ ^ ^1 0.2 0.2 0.2 0.05 25

# 签了第七柱的人，这一箭顺带把周围的掉落物点成两份 ——
# 借的是柱位自己的［点金］，不另写一份同味道的东西。
execute if entity @s[tag=rpg.pact,scores={rpg_pact=7}] at @s as @e[type=minecraft:item,distance=..8] at @s run function rpg:pact/p7_gild

# 付账。先看经验够不够，不够就拿命抵。
execute store result score #lv rpg_mam run xp query @s levels
execute if score #lv rpg_mam matches 5.. run return run function rpg:mammon/pay_xp
function rpg:mammon/pay_hp

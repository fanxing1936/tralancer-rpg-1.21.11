# 原罪的存续：加重、蔓延、倒数。
# 由 rpg:item/extra/skills 守卫调用 —— 没人拿枪、场上也没有带罪者时整段跳过。
execute as @e[tag=rpg.luci.sin,tag=rpg.hurt,scores={rpg_luci_cd=..0}] at @s run function rpg:item/extra/lucifer_sting
execute as @e[tag=rpg.luci.sin,scores={rpg_luci_sin=150}] at @s run function rpg:item/extra/lucifer_spread
execute as @e[tag=rpg.luci.sin,scores={rpg_luci_sin=100}] at @s run function rpg:item/extra/lucifer_spread
execute as @e[tag=rpg.luci.sin,scores={rpg_luci_sin=50}] at @s run function rpg:item/extra/lucifer_spread
execute as @e[tag=rpg.luci.sin] at @s run particle dust_color_transition{from_color:2257486,to_color:4895350,scale:1} ~ ~1 ~ 0.3 0.4 0.3 0.01 3

execute as @e[tag=rpg.luci.sin,scores={rpg_luci_cd=1..}] run scoreboard players remove @s rpg_luci_cd 1
execute as @e[tag=rpg.luci.sin,scores={rpg_luci_sin=1..}] run scoreboard players remove @s rpg_luci_sin 1
tag @e[tag=rpg.luci.sin,scores={rpg_luci_sin=..0}] remove rpg.luci.sin
# 蓄力冷却
execute as @a[scores={rpg_luci_use=1..}] run scoreboard players remove @s rpg_luci_use 1

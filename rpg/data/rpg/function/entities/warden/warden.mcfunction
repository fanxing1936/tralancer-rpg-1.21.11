
# Boss 热路径：空场只剩五个带类型/标签的存在性守卫。
execute as @e[tag=boss] unless score @s rpg_boom_id matches 1.. run function rpg:entities/warden/pseudo_id
execute if entity @e[tag=devil,limit=1] run function rpg:entities/warden/phase1
execute if entity @e[type=minecraft:vindicator,tag=devil2,limit=1] run function rpg:entities/warden/phase2
execute if entity @e[type=minecraft:armor_stand,tag=rpg.boss.slash,limit=1] run function rpg:entities/warden/slashes
execute if entity @e[type=minecraft:marker,tag=rpg.bossbar.probe,limit=1] run function rpg:entities/warden/bossbar_probe_tick
execute if entity @e[tag=boss,limit=1] run function rpg:entities/warden/bossbar_clock

# 米迦勒脊骨［谁似神］—— 由 rpg:advancement/item/michael_spine 在蓄力时触发。
# using_item 在按住期间每刻都响：断了两刻以上就算重新起手，蓄满 20 刻出手。
# 蓄力与冷却都对着 gametime 量，不依赖每刻倒数。
advancement revoke @s only rpg:item/michael_spine
execute store result score #now rpg_mi_tmp run time query gametime
scoreboard players operation #gap rpg_mi_tmp = #now rpg_mi_tmp
scoreboard players operation #gap rpg_mi_tmp -= @s rpg_mi_last
execute unless score @s rpg_mi_last = @s rpg_mi_last run scoreboard players set #gap rpg_mi_tmp 99
execute if score #gap rpg_mi_tmp matches 3.. run scoreboard players set @s rpg_mi_hold 0
scoreboard players operation @s rpg_mi_last = #now rpg_mi_tmp

# 冷却中：起手那一下提示一次，之后按住也不再响
execute if score @s rpg_mi_cd > #now rpg_mi_tmp if score @s rpg_mi_hold matches 0 run playsound minecraft:entity.villager.no player @s
execute if score @s rpg_mi_cd > #now rpg_mi_tmp run return run scoreboard players set @s rpg_mi_hold -1
execute if score @s rpg_mi_hold matches ..-1 run return 0

scoreboard players add @s rpg_mi_hold 1
execute if score @s rpg_mi_hold matches ..19 run function rpg:item/extra/michael_charge
execute if score @s rpg_mi_hold matches 20 run function rpg:item/extra/michael_cast

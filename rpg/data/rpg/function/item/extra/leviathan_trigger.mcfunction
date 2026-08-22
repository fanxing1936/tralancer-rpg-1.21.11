# 利维坦［沉锚］—— 由 rpg:advancement/item/leviathan 触发。
#
# `minecraft:using_item` 在按住右键期间**每刻都会响**，这正是蓄力需要的节拍：
# 每响一次攒一格，攒满 30 刻（1.5 秒）才真正抛锚。
# （包里的［王座］也是靠这个把 power_step 一格格加上去的。）
#
# 松手怎么判？trigger 每刻把 hold 设回 3，而每刻函数里递减它 ——
# 一旦停手，hold 会在 3 刻内归零，蓄力随之清空。
advancement revoke @s only rpg:item/leviathan
scoreboard players set @s rpg_levi_hold 3
execute if entity @s[scores={rpg_levi_charge=..30}] run scoreboard players add @s rpg_levi_charge 1

# 蓄力反馈：海水从脚下往上聚，越接近满蓄越急
execute at @s run particle bubble_column_up ~ ~0.1 ~ 0.4 0.1 0.4 0.02 2
execute at @s if entity @s[scores={rpg_levi_charge=10..}] run particle dust_color_transition{from_color:532802,to_color:1195644,scale:1} ~ ~0.9 ~ 0.45 0.7 0.45 0.02 3
execute at @s if entity @s[scores={rpg_levi_charge=20..}] run particle dust_color_transition{from_color:1195644,to_color:8374496,scale:1} ~ ~1.2 ~ 0.5 0.8 0.5 0.03 4
execute at @s if entity @s[scores={rpg_levi_charge=1}] run playsound minecraft:block.chain.place player @s ~ ~ ~ 1 0.6
execute at @s if entity @s[scores={rpg_levi_charge=10}] run playsound minecraft:block.chain.place player @s ~ ~ ~ 1 0.9
execute at @s if entity @s[scores={rpg_levi_charge=20}] run playsound minecraft:block.chain.place player @s ~ ~ ~ 1 1.3

# 满蓄的那一刻抛出去。之后 charge 会继续 +1 越过 30，
# 所以这条精确判等只会命中一次，按住不放不会连抛。
execute at @s if entity @s[scores={rpg_levi_charge=30}] run playsound minecraft:entity.elder_guardian.curse player @a[distance=..20] ~ ~ ~ 0.7 1.6
execute if entity @s[scores={rpg_levi_charge=30}] run function rpg:item/extra/leviathan_fire

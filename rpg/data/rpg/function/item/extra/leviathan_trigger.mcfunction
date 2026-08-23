# 利维坦［沉锚］—— 由 rpg:advancement/item/leviathan 触发。
#
# `minecraft:using_item` 在按住右键期间**每刻都会响**，这正是蓄力需要的节拍：
# 每响一次攒一格，攒满 30 刻（1.5 秒）才真正抛锚。
#
# 注意这里用的是无条件 `add`，不是 `execute if entity @s[scores=...]`：
# **选择器里的 scores 判定要求该记分项已经有值**，玩家第一次使用时
# rpg_levi_charge 根本不存在，条件恒假 —— 计数器永远起不来，技能也就永远放不出。
# `scoreboard players add` 在无值时会先当作 0，所以它总能起步。
# 攒过 30 之后继续涨没有坏处，下面的放锚判定是精确判等。
#
# 松手怎么判？trigger 每刻把 hold 顶回 3，每刻函数里递减它 ——
# 一旦停手，hold 会在 3 刻内归零，蓄力随之清空。
advancement revoke @s only rpg:item/leviathan
scoreboard players set @s rpg_levi_hold 3
scoreboard players add @s rpg_levi_charge 1

# 蓄力反馈：海水绕着脚下盘起来，越接近满蓄越高、越亮。
execute at @s run particle dust_color_transition{from_color:532802,to_color:1195644,scale:2} ~ ~0.2 ~ 0.75 0.06 0.75 0.03 12
execute at @s run particle bubble_column_up ~ ~0.1 ~ 0.55 0.05 0.55 0.08 6
execute at @s if entity @s[scores={rpg_levi_charge=10..}] run particle dust_color_transition{from_color:1195644,to_color:8374496,scale:2} ~ ~1 ~ 0.62 0.8 0.62 0.04 12
execute at @s if entity @s[scores={rpg_levi_charge=20..}] run particle splash ~ ~1.5 ~ 0.6 0.6 0.6 0.2 14
execute at @s if entity @s[scores={rpg_levi_charge=25..}] run particle dust_color_transition{from_color:8374496,to_color:16559622,scale:3} ~ ~1.9 ~ 0.5 0.45 0.5 0.06 16

# 进度条直接写在快捷栏上方，蓄到哪一档一目了然

execute at @s if entity @s[scores={rpg_levi_charge=1}] run playsound minecraft:block.chain.place player @s ~ ~ ~ 1 0.6
execute at @s if entity @s[scores={rpg_levi_charge=10}] run playsound minecraft:block.chain.place player @s ~ ~ ~ 1 0.9
execute at @s if entity @s[scores={rpg_levi_charge=20}] run playsound minecraft:block.chain.place player @s ~ ~ ~ 1 1.3

# 满蓄的那一刻抛出去。计数器随后继续 +1 越过 30，
# 所以这条精确判等只会命中一次，按住不放不会连抛。
execute at @s if entity @s[scores={rpg_levi_charge=30}] run playsound minecraft:entity.elder_guardian.curse player @a[distance=..20] ~ ~ ~ 0.8 1.6
execute if entity @s[scores={rpg_levi_charge=30}] run function rpg:item/extra/leviathan_fire


# 交给统一 HUD 渲染：声明占用，并把进度换算成 10 格
scoreboard players set @s rpg_hud 1
scoreboard players set @s rpg_hud_t 3
scoreboard players operation @s rpg_hud_p = @s rpg_levi_charge
scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
scoreboard players operation @s rpg_hud_p /= #hud_full rpg_hud
execute if entity @s[scores={rpg_hud_p=10..}] run scoreboard players set @s rpg_hud_p 10

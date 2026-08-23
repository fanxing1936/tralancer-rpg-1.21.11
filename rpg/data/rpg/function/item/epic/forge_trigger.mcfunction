# 熔火之锤［熔流］—— 由 rpg:advancement/item/forge 触发。
#
# `using_item` 在按住右键期间每刻都响，所以这里攒蓄力，攒满 30 刻才砸下去。
# 注意用的是无条件 `add`：选择器里的 scores 判定要求记分项**已经有值**，
# 第一次使用时它并不存在，条件恒假，计数器就永远起不来。
advancement revoke @s only rpg:item/forge
scoreboard players set @s rpg_forge_hold 3
scoreboard players add @s rpg_forge_chg 1

execute at @s run particle lava ~ ~0.3 ~ 0.45 0.1 0.45 0 2
execute at @s if entity @s[scores={rpg_forge_chg=12..}] run particle dust_color_transition{from_color:9445636,to_color:16553767,scale:2} ~ ~0.9 ~ 0.5 0.7 0.5 0.03 8
execute at @s if entity @s[scores={rpg_forge_chg=22..}] run particle flame ~ ~1.3 ~ 0.5 0.6 0.5 0.02 10
execute at @s if entity @s[scores={rpg_forge_chg=1}] run playsound minecraft:block.lava.ambient player @s ~ ~ ~ 1 0.7
execute at @s if entity @s[scores={rpg_forge_chg=12}] run playsound minecraft:block.lava.ambient player @s ~ ~ ~ 1 1.1
execute at @s if entity @s[scores={rpg_forge_chg=22}] run playsound minecraft:block.lava.ambient player @s ~ ~ ~ 1 1.5

# 精确判等，之后计数继续越过阈值，所以按住不放只砸一次
execute if entity @s[scores={rpg_forge_chg=30}] run function rpg:item/epic/forge_cast


# 交给统一 HUD 渲染：声明占用，并把进度换算成 10 格
scoreboard players set @s rpg_hud 2
scoreboard players set @s rpg_hud_t 3
scoreboard players operation @s rpg_hud_p = @s rpg_forge_chg
scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
scoreboard players operation @s rpg_hud_p /= #hud_full rpg_hud
execute if entity @s[scores={rpg_hud_p=10..}] run scoreboard players set @s rpg_hud_p 10

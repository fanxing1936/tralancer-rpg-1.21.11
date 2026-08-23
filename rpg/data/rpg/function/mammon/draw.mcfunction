# 正在拉弓。`using_item` 在按住期间每刻都响，所以这里就是逐刻的蓄力。
advancement revoke @s only rpg:item/mammon

# 这是新的一次拉弓吗？rpg_mam_dw 只活 2 刻，所以「上一刻还在拉」等价于它 >=1。
# 是新的一次就先清零 —— 蓄力**不跨箭累积**。
#
# 清零必须放在开始，不能放在结束：松手之后要 8 刻才关窗，
# 而连射的再次拉弓比这快得多，永远等不到那次清零。
execute if entity @s[scores={rpg_mam_dw=..0}] run scoreboard players set @s rpg_mam_c 0
scoreboard players set @s rpg_mam_dw 2
scoreboard players add @s rpg_mam_c 1

# 开一个窗口。松手之后的几刻里，rpg:mammon/watch 会去认那支离弦的箭 ——
# 弓没有「射出去了」这个触发器，只能反过来从箭那头认。
scoreboard players set @s rpg_mam_win 8

# 攒满的那一刻响一声，告诉你买断已经可以出手了
execute if entity @s[scores={rpg_mam_c=40}] run playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.6
execute if entity @s[scores={rpg_mam_c=40}] at @s run particle wax_on ~ ~1.2 ~ 0.3 0.3 0.3 0.05 20

# 交给统一 HUD 渲染：声明占用，并把进度换算成格数
scoreboard players set @s rpg_hud 5
scoreboard players set @s rpg_hud_t 3
scoreboard players operation @s rpg_hud_p = @s rpg_mam_c
scoreboard players operation @s rpg_hud_p *= #hud_seg rpg_hud
scoreboard players operation @s rpg_hud_p /= #mam_full rpg_hud
execute if entity @s[scores={rpg_hud_p=10..}] run scoreboard players set @s rpg_hud_p 10

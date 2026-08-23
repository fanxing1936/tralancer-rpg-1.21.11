# 往消息槽里写一个号，真正的渲染在 rpg:hud/msg。
# 直接写 actionbar 会和每刻渲染的进度条互相盖 —— 这条 actionbar
# 全局只有一行，所以全包只留一个出口。
scoreboard players set @s rpg_hud_m 27
scoreboard players set @s rpg_hud_mt 40

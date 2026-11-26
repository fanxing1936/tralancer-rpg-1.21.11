# 补满本段：血记在 rpg_dt_h（十分之一点）；载体自己的血永远顶在 1024，只用来量挨了多少
scoreboard players operation @s rpg_dt_h = @s rpg_dt_mx
scoreboard players operation @s rpg_dt_h *= #10 rpg_dt
function rpg:daath_fight/unit/top

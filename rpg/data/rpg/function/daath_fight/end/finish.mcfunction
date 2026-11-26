tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖哥林多前书 13:12〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"我们如今仿佛对着镜子观看，模糊不清；到那时，就要面对面了。","color":"#E6DFCF","bold":false,"italic":false}]
execute as @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/end/mine
scoreboard players set @a[tag=rpg.dt.me,limit=1] rpg_dt_ph 4
scoreboard players set @a[tag=rpg.dt.me,limit=1] rpg_dt_pt 0
function rpg:daath_fight/unit/vanish

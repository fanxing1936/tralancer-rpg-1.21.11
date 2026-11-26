# 夺到了（as/at 影子；挑战者 rpg.dt.me）：先夺武器，武器已夺或空手就夺盔甲
execute store result storage rpg:daath t.id int 1 run scoreboard players get @a[tag=rpg.dt.me,limit=1] rpg_fg_id
execute if score @s rpg_dt_sw matches ..0 if items entity @a[tag=rpg.dt.me,limit=1] weapon.mainhand #rpg:daath/weapon run return run function rpg:daath_fight/steal/take_w
execute if score @s rpg_dt_sa matches ..0 run function rpg:daath_fight/steal/take_a

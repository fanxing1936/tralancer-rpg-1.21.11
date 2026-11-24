scoreboard players remove #gd rpg_fo 1
execute if score #gd rpg_fo matches 1.. if block ~ ~-0.3 ~ #rpg:force/pass positioned ~ ~-0.5 ~ run return run function rpg:force/ground/star/step
execute align y run function rpg:force/ground/star/at

execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id
execute store result storage rpg:onboard tmp.r int 1 run random value 0..622
data modify storage rpg:onboard tmp.k set value "given"
function rpg:onboard/card/pick with storage rpg:onboard tmp
execute store result storage rpg:onboard tmp.r int 1 run random value 0..30
data modify storage rpg:onboard tmp.k set value "house"
function rpg:onboard/card/pick with storage rpg:onboard tmp
execute store result storage rpg:onboard tmp.r int 1 run random value 0..9
data modify storage rpg:onboard tmp.k set value "nation"
function rpg:onboard/card/pick with storage rpg:onboard tmp
function rpg:onboard/card/nomid with storage rpg:onboard tmp
execute store result storage rpg:onboard tmp.r int 1 run random value 0..51
data modify storage rpg:onboard tmp.k set value "mid"
execute store result score #mr rpg_ob run data get storage rpg:onboard tmp.r
execute if score #mr rpg_ob matches ..25 run function rpg:onboard/card/pick with storage rpg:onboard tmp

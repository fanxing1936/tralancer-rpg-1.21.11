$bossbar set rpg:daath_$(n) value $(v)
$data modify storage rpg:daath t.tx set from storage rpg:daath_bar b$(st)_$(v)
function rpg:daath_fight/bar/m2 with storage rpg:daath t

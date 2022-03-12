python train.py \
    --do-train \
    --eval-every 2000 \
    --run-name elliot-train \
    --finetune-path /vision/u/naagnes/github/robustqa/save/elliot-checkpoint \
    --train-datasets="race,relation_extraction,duorc" \
    --train-dir="datasets/oodomain_train" \
    --val-dir="datasets/oodomain_val" \
    --num-epochs 10 \
    --eval-every 10
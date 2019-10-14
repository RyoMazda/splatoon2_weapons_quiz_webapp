<template>
  <div class="home">
    <h1>Splatoon2 Weapons Quiz</h1>
    <div>
      <span>
        o: {{ numCorrect }}
      </span>
      <span>
        x: {{ numWrong }}
      </span>
      <span>
        / {{ numWeapons }}
      </span>
    </div>

    <div v-if="isFinished">
      終わりだし
    </div>
    <div v-else>
      <!--  Question  -->
      <div>
        <h2>You're familiar with this weapon, aren't you?</h2>
        <img :src="weaponId2ImagePath(weapon.id)" alt="target weapon">
      </div>

      <!--  Answer  -->
      <div v-if="showAnswer" class="showAnswer">
        <p>{{ weapon.name }} / {{ weapon.name_en }}</p>
        <div v-if="isCorrect">
          まあまあじゃん
        </div>
        <div v-else>
          違うし
        </div>

        <button @click="goToNextQuiz">Next</button>
      </div>

      <div>
        <div>
          <h3>Choose Correct Sub Weapon</h3>
          <ul>
            <li
                v-for="id in subWeaponIds" :key="id"
                @click="answerForm.subWeaponId = id"
            >
              <img
                  :src="subWeaponId2ImagePath(id)" alt="sub weapon"
                  :class="{
                  chosen: answerForm.subWeaponId === id,
                  answer: weapon.subWeaponId === id && showAnswer
                }"
              >
            </li>
          </ul>
        </div>
        <div>
          <h3>Choose Correct Special Weapon</h3>
          <ul>
            <li
                v-for="id in specialWeaponIds" :key="id"
                @click="answerForm.specialWeaponId = id"
            >
              <img
                  :src="specialWeaponId2ImagePath(id)" alt="special weapon"
                  :class="{
                  chosen: answerForm.specialWeaponId === id,
                  answer: weapon.specialWeaponId === id && showAnswer
                }"
              >
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import weapons from '@/weapons';

function createArray(start: number, end: number): number[] {
  const foo = [];
  for (let i = start; i <= end; i++) {
    foo.push(i);
  }
  return foo;
}

function getThreeDigitInteger(value: number): string {
  if (value < 10) {
    return '00' + value;
  } else if (value < 100) {
    return '0' + value;
  } else {
    return String(value);
  }
}

function shuffle(array: any[]): void {
  for (let i = array.length - 1; i >= 0; i--) {
    const rand = Math.floor( Math.random() * ( i + 1 ) );
    [array[i], array[rand]] = [array[rand], array[i]];
  }
}

function getNextWeapon(): Weapon | undefined {
  shuffle(weapons);
  return weapons.pop();
}


function getEmptyAnswerForm(): AnswerForm {
  return {
    subWeaponId: null,
    specialWeaponId: null,
  };
}


@Component({})
export default class Home extends Vue {
  public subWeaponIds: number[] = createArray(11, 23);
  public specialWeaponIds: number[] = createArray(8, 12).concat(createArray(14, 23));
  public numWeapons: number = weapons.length;
  public numCorrect: number = 0;
  public numWrong: number = 0;
  public weapon: Weapon | undefined = getNextWeapon();
  public answerForm: AnswerForm = getEmptyAnswerForm();

  public get showAnswer(): boolean {
    const showAnswer =  !!(this.answerForm.subWeaponId !== null && this.answerForm.specialWeaponId !== null);
    if (showAnswer) {
      window.scrollTo(0, 0);
    }
    return showAnswer;
  }
  public get isCorrect(): boolean {
    return !!(
      this.weapon &&
      this.answerForm.subWeaponId === this.weapon.subWeaponId &&
      this.answerForm.specialWeaponId === this.weapon.specialWeaponId
    );
  }
  public get isFinished(): boolean {
    return !this.weapon;
  }

  public weaponId2ImagePath(id: number): string {
    const ThreeDigitId = getThreeDigitInteger(id);
    return 'https://www.ikaclo.jp/common/images/weapons/main/weapon_' + ThreeDigitId + '.png';
  }

  public subWeaponId2ImagePath(id: number): string {
    const ThreeDigitId = getThreeDigitInteger(id);
    return 'https://www.ikaclo.jp/common/images/weapons/sub/sub_' + ThreeDigitId + '.png';
  }

  public specialWeaponId2ImagePath(id: number): string {
    const ThreeDigitId = getThreeDigitInteger(id);
    return 'https://www.ikaclo.jp/common/images/weapons/special/special_' + ThreeDigitId + '.png';
  }

  public goToNextQuiz(): void {
    if (this.isCorrect) {
      this.numCorrect += 1;
    } else {
      this.numWrong += 1;
    }
    this.answerForm = getEmptyAnswerForm();
    this.weapon = getNextWeapon();
  }

}
</script>


<style scoped lang="scss">
ul {
  padding: 0;
}
li{
  display: inline;
  list-style-type: none;
}
img {
  width: 80px;
  border: 5px white solid;
}
img.chosen {
  border: 5px blue solid;
}
img.answer {
  border: 10px red solid;
}

.showAnswer {
  font-size: x-large;
  font-weight: bold;
}
button {
  font-size: x-large;
}
</style>

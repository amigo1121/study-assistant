class TaskTreeNode {
  private _index: number;
  private _time: number;
  private _lazy: number;

  constructor(index: number = 0, time: number = 0) {
    this._index = index;
    this._time = time;
    this._lazy = 0;
  }

  // Getters
  get index(): number {
    return this._index;
  }

  get time(): number {
    return this._time;
  }

  get lazy(): number {
    return this._lazy;
  }

  // Setters
  set index(value: number) {
    this._index = value;
  }

  set time(value: number) {
    this._time = value;
  }

  set lazy(value: number) {
    this._lazy = value;
  }

  public clone(): TaskTreeNode {
    return new TaskTreeNode(this._index, this._time);
  }
}

interface Assignment {
  remained_time: number;
  [key: string]: any;
}

export class TaskPriorityTree {
  private _taskArray: TaskTreeNode[] = [];

  constructor(length: number) {
    this._taskArray = new Array<TaskTreeNode>(length);
  }

  // Return a TreeNode
  public getNode(id: number, left: number, right: number, index: number) {
    if (left > index || right < index) return null;
    if (left === right) return this._taskArray[id].clone();

    const mid = Math.floor((left + right) / 2);
    const left_child = this.getNode(id * 2, left, mid, index);
    const right_child = this.getNode(id * 2, mid + 1, right, index);

    if (!left_child) return right_child;
    if (!right_child) return left_child;
  }

  public getRoot() {
    return this._taskArray[1];
  }

  public build(
    id: number,
    left: number,
    right: number,
    arrValues: ReadonlyArray<Assignment>
  ) {
    if (left === right) {
      const time =
        arrValues[left].tasks.length > 0
          ? arrValues[left].remained_time
          : Infinity;
      this._taskArray[id] = new TaskTreeNode(left, time);
      return;
    }

    const mid = Math.floor((left + right) / 2);
    this.build(id * 2, left, mid, arrValues);
    this.build(id * 2 + 1, mid + 1, right, arrValues);

    const left_child = this._taskArray[id * 2];
    const right_child = this._taskArray[id * 2 + 1];
    this._taskArray[id] = new TaskTreeNode(0, 0);
    if (left_child.time < right_child.time) {
      this._taskArray[id].index = left_child.index;
      this._taskArray[id].time = left_child.time;
    } else {
      this._taskArray[id].index = right_child.index;
      this._taskArray[id].time = right_child.time;
    }
  }

  public update_single(
    id: number,
    left: number,
    right: number,
    newValue: number,
    newValueIndex: number
  ) {
    if (left > newValueIndex || right < newValueIndex) return;
    if (left === right) {
      this._taskArray[left].time = newValue;
      return;
    }
    const mid = Math.floor((left + right) / 2);

    this.lazy_down(id);
    this.update_single(id * 2, left, mid, newValue, newValueIndex);
    this.update_single(id * 2 + 1, mid + 1, right, newValue, newValueIndex);

    const left_child = this._taskArray[id * 2];
    const right_child = this._taskArray[id * 2 + 1];

    if (left_child.time < right_child.time) {
      this._taskArray[id] = left_child.clone();
    } else {
      this._taskArray[id] = right_child.clone();
    }
  }

  public lazy_down(id: number) {
    const lazy_value = this._taskArray[id].lazy;
    this._taskArray[id * 2].lazy += lazy_value;
    this._taskArray[id * 2].time += lazy_value;

    this._taskArray[id * 2 + 1].time += lazy_value;
    this._taskArray[id * 2 + 1].lazy += lazy_value;

    this._taskArray[id].lazy = 0;
  }

  public update_range(
    id: number,
    left: number,
    right: number,
    update_left_range: number,
    update_right_range: number,
    delta_value: number
  ) {
    if (update_left_range > update_right_range) return;
    if (right < update_left_range || update_right_range < left) return;
    if (update_left_range <= left && right <= update_right_range) {
      this._taskArray[id].time += delta_value;
      this._taskArray[id].lazy += delta_value;
      return;
    }

    const mid = Math.floor((left + right) / 2);

    this.lazy_down(id);
    this.update_range(
      id * 2,
      left,
      mid,
      update_left_range,
      update_right_range,
      delta_value
    );
    this.update_range(
      id * 2 + 1,
      mid + 1,
      right,
      update_left_range,
      update_right_range,
      delta_value
    );

    const left_child = this._taskArray[id * 2];
    const right_child = this._taskArray[id * 2 + 1];

    if (left_child.time < right_child.time) {
      this._taskArray[id].index = left_child.index;
      this._taskArray[id].time = left_child.time;
    } else {
      this._taskArray[id].index = right_child.index;
      this._taskArray[id].time = right_child.time;
    }
  }
}

let cottonShader;
let renderer;
let curTime = 0.0;
let cottonNum = 30;
let cottons = [];

const ColorPalette = Object.freeze({
  "white" : "#5A67D8",
  "lightblue" : "#4C51BF",
  "blue": "#434190",
  "darkblue": "#3C366B",
});

function preload(){
  cottonShader = loadShader("data/shader.vert", "data/shader.frag");
}

function windowResized() {
  resizeCanvas(windowWidth, 550); 
}

function setup() {
  renderer = createCanvas(windowWidth, 550, WEBGL);
  renderer.parent('sketch-holder');
  pixelDensity(1);

  for(let i=0; i<cottonNum; i++){
    let shift = random();
    let depth = map(shift, 0.0, 1.0, -400.0, 0.0);
    let size = map(shift, 0.0, 1.0, 10, 50);
    let cotton = new Cotton(createVector(random(-width * 0.5, width * 0.5), random(-height * 0.5, height * 0.5), depth), size, shift);
    cottons.push(cotton);
  }
}

function draw() {
  let bluecol = lerpColor(color(ColorPalette.blue), color(ColorPalette.darkblue), map(sin(radians(curTime * 20)), -1.0, 1.0, 0.0, 1.0));
  ortho();

  background(color(ColorPalette.darkblue));
  // lights();
  cottonShader.setUniform("u_col1", color(ColorPalette.white)._array);
  cottonShader.setUniform("u_col2", color(ColorPalette.darkblue)._array);


  for(let i=0; i<cottons.length; i++){
    let cotton = cottons[i];
    cotton.update();
    cotton.draw();
  }
  curTime += deltaTime * 0.001;

  let c1 = color(45,39,89,0);
  let c2 = color(45,40,89,100)

  setGradient(c1,c2,0,height/2);
  
  push();
  noStroke();
  fill(250,250,250, 20);
  ellipse(mouseX-width/2,mouseY-height/2,250,250);
  pop();
}

function setGradient(c1,c2,top,bottom) {

  push();
  for (var y = top; y < bottom; y++) {
    var inter = map(y, top, bottom, 0, 1);
    var c = lerpColor(c1, c2, inter);
    stroke(c);
    line(-width/2, y, width/2, y);
  }
  pop();
}

class Cotton{
  constructor(pos, size, shift){
    this.pos = pos;
    this.size = size;
    this.shift = shift;//random(100.0);
    this.geom = SphereGeometry(size, 20, 20);
    this.upspeed = 2.0;
    this.rand = random(1000.0);
  }

  update(){
    let speed = map(this.shift, 0.0, 1.0, -this.upspeed * 0.5, -this.upspeed);
    let sideshift = 0.01;
    let shiftnoise = noise(this.pos.x * sideshift + this.rand, this.pos.y * sideshift+ this.rand, this.pos.z * sideshift + this.rand) - 0.3;
    this.pos.add(createVector(shiftnoise * 5.0, speed, 0));

    if(this.pos.y < -height * 0.5 - this.size){
      this.pos.y = height * 0.5 + this.size;
    }

    if(this.pos.x > width * 0.5 - this.size * 2){
      this.pos.x -= 1;
    }else if(this.pos.x < -width * 0.5 + this.size * 2){
      this.pos.x += 1;
    }
    
    let vec = createVector(mouseX - width/2, mouseY - height/2);
    let xyPosVec = createVector(this.pos.x, this.pos.y);
    let distance = vec.dist(xyPosVec);
    var mappedDistance = map(distance, 250, 0, -0.5, -2.5);
    if(distance < 250) {
      vec.sub(xyPosVec);
      vec.normalize();
      vec.mult(mappedDistance);
      this.pos.add(vec);
    }
    let smooth = map(this.shift, 0.0, 1.0, 0.05, 0.025);
    modifySphereGeometry(this.geom, 50, 0.5, smooth, this.rand);
    this.geom.computeNormals();
  }

  draw(){
    push();
    translate(this.pos.x, this.pos.y, this.pos.z);
    // fill(255);
    // stroke(0);
    shader(cottonShader);
    renderer.createBuffers("custom", this.geom);
    renderer.drawBuffers("custom");
    pop();
  }
}

function modifySphereGeometry(geom, offset, speed, smoothness, shift){
  noiseDetail(2, 0.2);
  for(let i=0; i<geom.origvertices.length; i++){
    let origvertex = geom.origvertices[i];
    let vertex = geom.vertices[i];

    let time = curTime * speed;
    let scale = smoothness;
    let noiseval = noise(origvertex.x * scale + time + 23.52 + shift, origvertex.y * scale + time + 62.35 + shift, origvertex.z * scale + time + 16.62 + shift);

    let norm = origvertex.copy();
    norm.normalize();
    norm.mult(offset * noiseval);
    geom.vertices[i] = origvertex.copy().add(norm);
  }
}


function SphereGeometry( radius, widthSegments, heightSegments){//}, phiStart, phiLength, thetaStart, thetaLength ) {
  let geom = new p5.Geometry();

  radius = radius || 1;

  widthSegments = Math.max( 3, Math.floor( widthSegments ) || 8 );
  heightSegments = Math.max( 2, Math.floor( heightSegments ) || 6 );

  phiStart = 0;
  phiLength = Math.PI * 2;

  thetaStart = 0;
  thetaLength = Math.PI;

  var thetaEnd = Math.min( thetaStart + thetaLength, Math.PI );

  var ix, iy;

  var index = 0;
  var grid = [];

  // buffers

  var indices = [];
  var vertices = [];
  var origvertices = [];
  var normals = [];
  var uvs = [];

  // generate vertices, normals and uvs

  for ( iy = 0; iy <= heightSegments; iy ++ ) {

    var verticesRow = [];

    var v = iy / heightSegments;

    // special case for the poles

    var uOffset = 0;

    if ( iy == 0 && thetaStart == 0 ) {

      uOffset = 0.5 / widthSegments;

    } else if ( iy == heightSegments && thetaEnd == Math.PI ) {

      uOffset = - 0.5 / widthSegments;

    }

    for ( ix = 0; ix < widthSegments; ix ++ ) {

      var u = ix / widthSegments;

      // vertex
      var vertex = createVector();
      var normal = createVector();
      vertex.x = - radius * Math.cos( phiStart + u * phiLength ) * Math.sin( thetaStart + v * thetaLength );
      vertex.y = radius * Math.cos( thetaStart + v * thetaLength );
      vertex.z = radius * Math.sin( phiStart + u * phiLength ) * Math.sin( thetaStart + v * thetaLength );

      vertices.push( vertex);
      origvertices.push(vertex.copy());

      // normal

      normal = vertex.copy();
      normal.normalize();
      normals.push( normal );

      // uv

      uvs.push( [u + uOffset, 1 - v] );

      verticesRow.push( index ++ );

    }

    grid.push( verticesRow );

  }

  // indices

  for ( iy = 0; iy < heightSegments; iy ++ ) {

    for ( ix = 0; ix < widthSegments; ix ++ ) {

      var a = grid[ iy ][ (ix + 1) % grid[iy].length ];
      var b = grid[ iy ][ ix ];
      var c = grid[ iy + 1 ][ ix ];
      var d = grid[ iy + 1 ][ (ix + 1) % grid[iy + 1].length ];

      if ( iy !== 0 || thetaStart > 0 ) indices.push( [a, b, d] );
      if ( iy !== heightSegments - 1 || thetaEnd < Math.PI ) indices.push( [b, c, d] );

    }

  }

  // build geometry
  
  geom.vertices = vertices;
  geom.origvertices = origvertices;
  geom.uvs = uvs;
  geom.faces = indices;
  geom.vertexNormals = normals;
  geom.computeNormals();


  return geom;
}

const db = require("../db");
const seed = [
  {
    nom: "email",
    adresse: "rue d'adresse",
    email: "email@email.com",
    pays: "France",
    status: "Actif",
    role: "Client",
  },
  {
    nom: "Malik",
    adresse: "rue d'adresse",
    email: "dass@email.com",
    pays: "France",
    status: "Inactif",
    role: "Client",
  },
  {
    nom: "email",
    adresse: "rue d'adresse",
    email: "email@email.com",
    pays: "France",
    status: "Actif",
    role: "Admin",
  },
  {
    nom: "presta",
    adresse: "rue d'adresse",
    email: "presta@email.com",
    pays: "France",
    status: "Actif",
    role: "Presta",
  },
];

(async () => {
  try {
    await db.schema.dropTableIfExists("users");
    await db.schema.withSchema("public").createTable("users", (table) => {
      table.increments();
      table.string("nom");
      table.string("adresse");
      table.string("email");
      table.string("pays");
      table.string("status");
      table.string("role");
    });
    console.log("Created users table!");
    for (let index = 0; index < seed.length; index++) {
      const element = seed[index];
      await db.select().from("users").insert(element).returning("*");
    }
    // process.exit(0);
    console.log("users save:");
    process.exit(0);
  } catch (err) {
    console.log(err);
    // process.exit(1);
  }
})();
